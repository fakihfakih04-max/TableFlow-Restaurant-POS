TableFlow Restaurant POS — Xprinter LAN kitchen + USB customer receipt

FILES
- index.html: restaurant POS interface.
- print_agent.py: local helper for LAN kitchen tickets and Windows USB customer receipts.
- start_print_agent.bat: installs pywin32 if needed, then starts the helper.

CUSTOMER RECEIPT — USB
1. Make sure the Xprinter USB is connected to the cashier PC and already prints a Windows test page.
2. Close any older TableFlow print-agent console windows.
3. Double-click start_print_agent.bat. Keep the black console window open while using the POS. The first run may install pywin32.
4. Open index.html in Chrome or Edge, go to Settings.
5. Under Customer receipt printing, choose “Automatic Windows USB printer”.
6. Click “Load Windows printers” and select the exact Xprinter queue name from the list.
7. Click “Save settings”. Then click “Print test receipt”. Confirm a short test receipt comes out.
8. When an order is paid/checked out, the customer receipt is sent to the selected USB printer automatically. A newly created order paid immediately also sends a kitchen ticket according to the kitchen-print settings.

CUSTOMER RECEIPT CONTENT
- Restaurant name, invoice number, date/time, order type and table/customer details when available.
- Items, quantities, extras/modifiers, item prices, subtotal, tax/service/discount, total in USD and LBP, exchange rate, payment method, and receipt footer.
- Prices are currently stored in USD and converted to LBP using the configured exchange rate.

KITCHEN TICKET — LAN
1. Connect the kitchen Xprinter to the router by Ethernet and find its actual IP from its network/self-test page or the router's DHCP list.
2. In Settings, choose Automatic Xprinter LAN, enter that IP and port (normally 9100), and keep the print service URL at http://127.0.0.1:8765.
3. The LAN ticket sends order details and modifiers without customer prices.

PRINT SERVICE CHECK
- Open http://127.0.0.1:8765/health on the cashier PC; JSON with "ok": true means the helper is running.
- The printer list is available at http://127.0.0.1:8765/printers.

IMPORTANT LIMITATIONS
- This is a single-device prototype; orders do not yet synchronize across computers.
- The helper must run on the same Windows PC as the browser POS.
- USB RAW printing assumes the installed Windows Xprinter queue accepts ESC/POS data. This has not been physically tested on your printer yet; use the test receipt before taking real orders.
- Receipt/kitchen text uses a basic Western code page. Arabic text support depends on the Xprinter model and code page and must be tested; English item names are the safest first test.
- Do not guess a LAN printer IP. Use the printer's network test page/router list.

WINDOWS APP MODE + USERS/LOGIN
See README_WINDOWS_APP_LOGIN.txt. Use START_TABLEFLOW_WINDOWS_APP.bat to open a dedicated Edge app window and start the print agent. Default pilot login is admin / 1234; change it after first login in Users & Login. This is a pilot launcher, not a compiled commercial EXE/MSI.


CUSTOMER MENU QR + ONLINE DELIVERY
See README_CUSTOMER_MENU_ONLINE.txt. Run server.py via uvicorn; the POS must be opened from the same server origin for the simple local setup.
