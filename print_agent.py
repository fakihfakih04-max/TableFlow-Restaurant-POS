#!/usr/bin/env python3
"""
TableFlow Xprinter LAN + USB Print Agent
Runs locally on the POS computer. Sends ESC/POS bytes to Xprinter LAN port (normally 9100).
Python standard library only.
"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json, socket, time, re

HOST = "127.0.0.1"
PORT = 8765
MAX_BODY = 1_000_000

def win32print_module():
    try:
        import win32print
        return win32print
    except ImportError:
        raise RuntimeError("Windows USB printing needs pywin32. Run start_print_agent.bat again to install it.")

def clean(value, max_len=160):
    text = str(value or "")
    text = text.replace("\x00", "").replace("\r", " ").replace("\n", " ")
    return text[:max_len]

def escpos_text(text):
    # Basic Western/English text is safe for most Xprinter ESC/POS models.
    # Arabic encoding varies by printer firmware/code page; use English names or configure a code page.
    return clean(text, 240).encode("cp437", errors="replace")

def line(text=""):
    return escpos_text(text) + b"\n"

def build_ticket(d):
    out = bytearray()
    out += b"\x1b@"                 # initialize
    out += b"\x1ba\x01"             # center
    out += b"\x1bE\x01"             # bold on
    out += line(d.get("restaurant", "Restaurant"))
    out += line("KITCHEN ORDER")
    out += line("#" + clean(d.get("order_id", "?"), 20))
    out += b"\x1bE\x00"
    out += line("--------------------------------")
    out += b"\x1ba\x00"             # left
    out += line("Type: " + clean(d.get("type", "")))
    if d.get("table"):
        out += line("Table: " + clean(d.get("table")))
    if d.get("customer"):
        out += line("Customer: " + clean(d.get("customer")))
    if d.get("phone"):
        out += line("Phone: " + clean(d.get("phone")))
    if d.get("address"):
        out += line("Address: " + clean(d.get("address"), 220))
    out += line("Time: " + clean(d.get("created_at", "")))
    out += line("--------------------------------")
    items = d.get("items") or []
    for item in items:
        qty = clean(item.get("qty", 1), 12)
        name = clean(item.get("name") or item.get("display_name") or "Item")
        out += b"\x1bE\x01"
        out += line(f"{qty} x {name}")
        out += b"\x1bE\x00"
        for extra in item.get("modifiers") or []:
            out += line("  + " + clean(extra))
        if item.get("note"):
            out += b"\x1bE\x01"
            out += line("  NOTE: " + clean(item["note"], 220))
            out += b"\x1bE\x00"
    if d.get("note"):
        out += line("--------------------------------")
        out += b"\x1bE\x01"
        out += line("ORDER NOTE:")
        out += line(clean(d["note"], 240))
        out += b"\x1bE\x00"
    out += line("--------------------------------")
    out += b"\x1ba\x01"
    out += line("Kitchen copy")
    out += b"\n\n\n"
    out += b"\x1dV\x00"             # full cut (ignored by some models)
    return bytes(out)

def money_usd(value):
    return "$" + format(float(value or 0), ",.2f")

def money_lbp(value):
    return "LL " + format(int(round(float(value or 0))), ",")

def receipt_line(text=""):
    return escpos_text(clean(text, 240)) + b"\n"

def build_receipt(d):
    out = bytearray(b"\x1b@")
    out += b"\x1ba\x01\x1bE\x01"
    out += receipt_line(d.get("restaurant", "Restaurant"))
    out += b"\x1bE\x00"
    if d.get("test"):
        out += receipt_line("USB PRINTER TEST")
        out += receipt_line("TableFlow Restaurant POS")
        out += receipt_line("If you can read this, printing works.")
        out += b"\x1ba\x00"
        out += receipt_line("------------------------------------------")
        out += receipt_line("Connection: Windows USB printer queue")
        out += receipt_line("------------------------------------------")
        out += b"\x1ba\x01"
        out += receipt_line(d.get("footer", "Test successful"))
        out += b"\n\n\n\x1dV\x00"
        return bytes(out)

    out += receipt_line("CUSTOMER RECEIPT")
    out += receipt_line("Invoice #" + clean(d.get("order_id", "?"), 20))
    out += b"\x1bE\x00\x1ba\x00"
    out += receipt_line("------------------------------------------")
    out += receipt_line("Type: " + clean(d.get("type", "")))
    if d.get("table"):
        out += receipt_line("Table: " + clean(d.get("table")))
    if d.get("customer"):
        out += receipt_line("Customer: " + clean(d.get("customer")))
    if d.get("phone"):
        out += receipt_line("Phone: " + clean(d.get("phone")))
    if d.get("address"):
        out += receipt_line("Address: " + clean(d.get("address"), 220))
    out += receipt_line("Date: " + clean(d.get("created_at", ""), 80))
    out += receipt_line("------------------------------------------")
    out += b"\x1bE\x01"
    for item in d.get("items") or []:
        qty = float(item.get("qty", 1) or 1)
        name = clean(item.get("name") or item.get("display_name") or "Item", 150)
        price = float(item.get("price", 0) or 0)
        out += receipt_line(f"{qty:g} x {name}")
        if item.get("modifiers"):
            out += b"\x1bE\x00"
            for extra in item.get("modifiers") or []:
                out += receipt_line("  + " + clean(extra, 100))
            out += b"\x1bE\x01"
        if item.get("note"):
            out += b"\x1bE\x00"
            out += receipt_line("  Note: " + clean(item.get("note"), 180))
            out += b"\x1bE\x01"
        out += receipt_line("  " + money_usd(price) + " each  |  " + money_usd(price * qty))
    out += b"\x1bE\x00"
    out += receipt_line("------------------------------------------")
    out += receipt_line("Subtotal: " + money_usd(d.get("subtotal", 0)))
    if float(d.get("tax", 0) or 0):
        out += receipt_line("Tax:      " + money_usd(d.get("tax", 0)))
    if float(d.get("service", 0) or 0):
        out += receipt_line("Service:  " + money_usd(d.get("service", 0)))
    if float(d.get("discount", 0) or 0):
        out += receipt_line("Discount: -" + money_usd(d.get("discount", 0)))
    out += b"\x1bE\x01"
    out += receipt_line("TOTAL:    " + money_usd(d.get("total", 0)))
    out += receipt_line("TOTAL:    " + money_lbp(d.get("total_lbp", 0)))
    out += b"\x1bE\x00"
    out += receipt_line("Rate: 1 USD = " + format(float(d.get("rate", 89500) or 89500), ",.0f") + " LBP")
    out += receipt_line("Payment: " + clean(d.get("payment", "Cash")))
    if d.get("payment_currency"):
        out += receipt_line("Payment currency: " + clean(d.get("payment_currency")))
    out += receipt_line("------------------------------------------")
    out += b"\x1ba\x01"
    if d.get("footer"):
        out += receipt_line(d.get("footer"))
    out += receipt_line("Thank you for your visit!")
    out += b"\n\n\n"
    # Kick the cash drawer through the receipt printer's drawer port (ESC/POS).
    # Most Xprinter-compatible drawers use pin 2; some models require pin 5 or different pulse timing.
    if bool(d.get("open_cash_drawer", True)) and not d.get("test"):
        out += b"\x1b\x70\x00\x19\xfa"  # ESC p m=0 t1=25 t2=250
    out += b"\x1dV\x00"
    return bytes(out)

def send_to_windows_printer(printer_name, payload):
    win32print = win32print_module()
    printer_name = str(printer_name or "").strip()
    if not printer_name:
        raise ValueError("Select the Xprinter USB from the Windows printer list")
    handle = win32print.OpenPrinter(printer_name)
    try:
        job = win32print.StartDocPrinter(handle, 1, ("TableFlow Customer Receipt", None, "RAW"))
        try:
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, payload)
            win32print.EndPagePrinter(handle)
        finally:
            win32print.EndDocPrinter(handle)
    finally:
        win32print.ClosePrinter(handle)
    return len(payload)

class Handler(BaseHTTPRequestHandler):
    server_version = "TableFlowPrintAgent/1.0"

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def send_json(self, status, obj):
        raw = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/health", "/"):
            self.send_json(200, {"ok": True, "service": "TableFlow Xprinter LAN + USB Print Agent"})
        elif self.path == "/printers":
            try:
                win32print = win32print_module()
                flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
                names = sorted({row[2] for row in win32print.EnumPrinters(flags) if len(row) > 2 and row[2]})
                self.send_json(200, {"ok": True, "printers": names})
            except Exception as exc:
                self.send_json(500, {"ok": False, "error": str(exc)})
        else:
            self.send_json(404, {"ok": False, "error": "Not found"})

    def do_POST(self):
        if self.path not in ("/print", "/print-usb"):
            self.send_json(404, {"ok": False, "error": "Not found"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > MAX_BODY:
                self.send_json(400, {"ok": False, "error": "Invalid request size"})
                return
            raw = self.rfile.read(size)
            data = json.loads(raw.decode("utf-8"))
            if self.path == "/print-usb":
                payload = build_receipt(data)
                sent = send_to_windows_printer(data.get("printer_name", ""), payload)
                self.send_json(200, {"ok": True, "order_id": data.get("order_id"), "bytes_sent": sent, "printer_name": data.get("printer_name")})
                return
            ip = str(data.get("printer_ip", "")).strip()
            port = int(data.get("printer_port", 9100))
            # Restrict destination to private/local IPv4 addresses to avoid misuse.
            import ipaddress
            addr = ipaddress.ip_address(ip)
            if addr.version != 4 or not (addr.is_private or addr.is_link_local):
                self.send_json(400, {"ok": False, "error": "Printer IP must be a private LAN IPv4 address"})
                return
            if not 1 <= port <= 65535:
                self.send_json(400, {"ok": False, "error": "Invalid printer port"})
                return
            payload = build_ticket(data)
            with socket.create_connection((ip, port), timeout=4) as sock:
                sock.settimeout(4)
                sock.sendall(payload)
            self.send_json(200, {"ok": True, "order_id": data.get("order_id"), "bytes_sent": len(payload)})
        except socket.timeout:
            self.send_json(502, {"ok": False, "error": "Printer connection timed out; check IP, port and power"})
        except ConnectionRefusedError:
            self.send_json(502, {"ok": False, "error": "Printer refused connection; check that RAW printing is enabled on the configured port"})
        except Exception as exc:
            self.send_json(400, {"ok": False, "error": str(exc)})

def main():
    print("=" * 58)
    print("TableFlow Xprinter LAN + USB Print Agent")
    print(f"Listening at http://{HOST}:{PORT}")
    print("Keep this window open while using Restaurant POS.")
    print("Test service: open http://127.0.0.1:8765/health")
    print("Windows USB printer list: http://127.0.0.1:8765/printers")
    print("=" * 58)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
