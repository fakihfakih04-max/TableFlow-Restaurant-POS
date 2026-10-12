TABLEFLOW RESTAURANT POS — WINDOWS APP WINDOW + USER ROLE SECURITY
===============================================================

OPEN THE PROGRAM
1. Extract the entire ZIP folder to a permanent folder such as C:\TableFlowRestaurant.
2. Install Microsoft Edge and Python 3 on the Windows PC.
3. Double-click START_TABLEFLOW_WINDOWS_APP.bat. The POS opens in a dedicated Edge app window without normal browser tabs/address bar. The print service opens separately; keep it open for printer use.
4. Optional: run CREATE_DESKTOP_SHORTCUT.bat to create a desktop shortcut.

LOGIN
- The username field is a combo box listing active users. Choose your own user and enter that user's PIN/password.
- Initial setup account: admin / 1234. Change it before staff use.
- To create staff accounts: Admin login > Users & Login > Add user.

ROLE ACCESS
- Admin: all modules and user management.
- Manager: orders, tables, kitchen, delivery, menu, inventory, reports and settings; no user management.
- Cashier: POS screen only. Cannot open other modules through the normal app navigation.
- Lock / Logout returns to the user-selection login screen. Disabled users are not listed and cannot log in.

IMPORTANT SECURITY LIMITATION
This is an offline HTML pilot. PINs/user data are stored in the local browser profile, and client-side role checks are not tamper-proof. It is NOT production-grade authentication. For real commercial security and multiple PCs, the app must validate users and permissions on a protected central server/database.

PRINTERS
Configure the USB receipt printer and LAN kitchen printer in Settings and physically test both. Arabic thermal output depends on the exact printer model.


RECIPE COSTING (SANDWICHES / PLATES)
1. Login as Admin or Manager and open Menu & Recipes.
2. Add or edit a sandwich/plate and enter the selling price.
3. Under Recipe / Bill of Materials, press + Ingredient for each ingredient used in ONE portion.
4. Choose an inventory ingredient and enter the portion quantity using that ingredient's stock unit (for example 0.25 kg chicken, 0.20 kg potatoes, 0.03 kg garlic sauce, 0.015 L oil).
5. The POS calculates ingredient cost, gross profit per portion (selling price minus ingredient cost), and gross margin. Keep inventory unit costs updated from real purchase costs.
6. When an order is sent to the kitchen, recipe ingredients are deducted from local inventory. If the order is cancelled through the table order dialog, the deducted recipe stock is returned.
7. This calculation does not yet include packaging, labor, utilities, waste, tax, or the ingredient consumption of optional extras; account for those separately before relying on net profit.
