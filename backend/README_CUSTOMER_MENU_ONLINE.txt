TABLEFLOW CUSTOMER MENU: QR TABLES + ONLINE DELIVERY (PILOT)

WHAT IS INCLUDED
- server.py: FastAPI API and shared SQLite database for published menu and customer orders.
- customer_menu.html: mobile-friendly customer ordering page.
- index.html: POS bridge publishes menu and polls incoming customer orders every 10 seconds.

LOCAL TEST ON ONE PC
1. Install Python 3.11+ 64-bit.
2. Open this folder in Command Prompt.
3. Set a private token: set TABLEFLOW_ADMIN_TOKEN=replace-with-a-long-random-secret
4. Run: python -m pip install -r requirements-online.txt
5. Run: python -m uvicorn server:app --host 0.0.0.0 --port 8000
6. Open cashier POS at http://127.0.0.1:8000/ and customer menu at http://127.0.0.1:8000/customer
7. In POS > Settings, click Configure Customer Menu Server. URL http://127.0.0.1:8000, token same as step 3.
8. Click Publish menu to customer phones. Test a customer order; it should arrive in POS and kitchen on the next poll.
9. For a phone on same Wi-Fi, use http://YOUR-CASHIER-PC-LAN-IP:8000/customer . Table QR example: http://YOUR-CASHIER-PC-LAN-IP:8000/customer?table=1 . Get LAN IP via ipconfig. Generate a QR code from each table URL. Allow Python through Windows Firewall for private networks.

ONLINE DELIVERY FROM OUTSIDE THE RESTAURANT
Deploy server.py and these files to a public HTTPS ASGI host, set TABLEFLOW_ADMIN_TOKEN to a strong secret in environment variables, and configure persistent database storage. Set POS server URL to the deployed HTTPS URL. A free host with ephemeral storage may lose SQLite data; use persistent disk or managed PostgreSQL before production.

LIMITATIONS / SAFETY
This is a pilot bridge, not full production multi-device synchronization. It shares published menu and incoming customer orders only; the POS still stores its own full sales/inventory state in localStorage, so paid status, stock, kitchen status, and all other POS data are not yet bidirectionally synchronized across devices. Keep the cashier POS open. Do not expose publicly without HTTPS, strong secrets, rate limits, authentication, persistent DB and backups.
