from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Any
from pathlib import Path
import sqlite3, json, os, time, secrets
BASE=Path(__file__).resolve().parent
DB_PATH=Path(os.environ.get('TABLEFLOW_DB_PATH',str(BASE/'tableflow_shared.db')))
ADMIN_TOKEN=os.environ.get('TABLEFLOW_ADMIN_TOKEN','')
app=FastAPI(title='TableFlow Customer Ordering API')
def db():
 c=sqlite3.connect(DB_PATH,timeout=20); c.row_factory=sqlite3.Row
 c.execute('PRAGMA journal_mode=WAL')
 c.execute('CREATE TABLE IF NOT EXISTS menu_snapshot (id INTEGER PRIMARY KEY CHECK(id=1), payload TEXT NOT NULL, updated_at INTEGER NOT NULL)')
 c.execute('CREATE TABLE IF NOT EXISTS customer_orders (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT NOT NULL, status TEXT NOT NULL DEFAULT \'sent\', created_at INTEGER NOT NULL, source_ref TEXT UNIQUE)'); c.commit(); return c
class MenuPayload(BaseModel):
 items:list[dict[str,Any]]=Field(default_factory=list); categories:list[str]=Field(default_factory=list); settings:dict[str,Any]=Field(default_factory=dict)
class OrderPayload(BaseModel):
 type:str='Delivery'; tableId:str|None=None; customer:str=''; phone:str=''; address:str=''; items:list[dict[str,Any]]; note:str=''; tax:float=0; sourceRef:str|None=None

def auth(request):
 if not ADMIN_TOKEN or not secrets.compare_digest(request.headers.get('x-tableflow-admin',''),ADMIN_TOKEN): raise HTTPException(401,'Admin token is not configured or is incorrect.')
@app.get('/api/health')
def health(): return {'ok':True,'service':'TableFlow Customer Menu API'}
@app.get('/api/menu')
def get_menu():
 with db() as c:
  r=c.execute('SELECT payload,updated_at FROM menu_snapshot WHERE id=1').fetchone()
  return ({**json.loads(r['payload']),'updatedAt':r['updated_at']} if r else {'items':[],'categories':[],'settings':{'name':'TableFlow Restaurant'}})
@app.post('/api/menu/publish')
def publish_menu(payload:MenuPayload,request:Request):
 auth(request); body={'items':[i for i in payload.items if i.get('available',True)],'categories':payload.categories,'settings':{'name':payload.settings.get('name','TableFlow Restaurant'),'tax':payload.settings.get('tax',0)}}
 with db() as c: c.execute('INSERT INTO menu_snapshot(id,payload,updated_at) VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at',(json.dumps(body,ensure_ascii=False),int(time.time()*1000)))
 return {'ok':True,'items':len(body['items'])}
@app.post('/api/orders')
def create_order(order:OrderPayload):
 if not order.items: raise HTTPException(400,'Add at least one item.')
 if not order.customer.strip() or not order.phone.strip(): raise HTTPException(400,'Name and phone are required.')
 if order.type.lower()=='delivery' and not order.address.strip(): raise HTTPException(400,'Delivery address is required.')
 published=get_menu(); valid={str(i.get('id')):i for i in published.get('items',[])}; lines=[]; subtotal=0
 for line in order.items:
  item=valid.get(str(line.get('id'))); qty=int(line.get('qty',0))
  if not item or qty<1: raise HTTPException(400,'Menu item unavailable; refresh the menu.')
  price=float(item.get('price',0)); subtotal+=price*qty; lines.append({'id':item.get('id'),'name':item.get('name','Item'),'price':price,'qty':qty,'note':str(line.get('note',''))})
 ref=order.sourceRef or secrets.token_hex(12); now=int(time.time()*1000)
 body={'id':None,'serverOrderId':None,'type':order.type,'tableId':order.tableId,'customer':order.customer.strip(),'phone':order.phone.strip(),'address':order.address.strip(),'items':lines,'note':order.note,'status':'sent','payment':'','tax':round(subtotal*max(0,min(float(order.tax),100))/100,2),'service':0,'discount':0,'createdAt':now,'source':'Customer menu','sourceRef':ref}
 with db() as c:
  try: cur=c.execute('INSERT INTO customer_orders(payload,status,created_at,source_ref) VALUES(?,?,?,?)',(json.dumps(body,ensure_ascii=False),'sent',now,ref))
  except sqlite3.IntegrityError: raise HTTPException(409,'Order already submitted.')
  body['id']=body['serverOrderId']=cur.lastrowid; c.execute('UPDATE customer_orders SET payload=? WHERE id=?',(json.dumps(body,ensure_ascii=False),cur.lastrowid))
 return {'ok':True,'orderId':body['id'],'status':'sent'}
@app.get('/api/orders/pending')
def pending(request:Request):
 auth(request)
 with db() as c: return {'orders':[json.loads(r['payload']) for r in c.execute("SELECT payload FROM customer_orders WHERE status='sent' ORDER BY id").fetchall()]}
@app.post('/api/orders/{oid}/ack')
def ack(oid:int,request:Request):
 auth(request)
 with db() as c:
  r=c.execute('SELECT payload FROM customer_orders WHERE id=?',(oid,)).fetchone()
  if not r: raise HTTPException(404,'Order not found')
  body=json.loads(r['payload']); body['syncedToPos']=True; c.execute("UPDATE customer_orders SET status='received',payload=? WHERE id=?",(json.dumps(body,ensure_ascii=False),oid))
 return {'ok':True}
@app.get('/customer')
def customer(): return FileResponse(BASE/'customer_menu.html')
@app.get('/')
def home(): return FileResponse(BASE/'index.html')
