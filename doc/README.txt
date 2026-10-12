TABLEFLOW CUSTOMER-ONLY GITHUB PAGES SITE

This folder is intended for the GitHub Pages /docs source.
The only public page is the customer menu, not the restaurant admin/POS screen.

IMPORTANT:
1. GitHub Pages is static hosting and cannot save orders by itself.
2. Deploy the backend-service files to an HTTPS host with persistent database storage.
3. Edit index.html and replace API_BASE with the actual HTTPS backend URL.
4. Upload this folder's index.html into the repository's docs/ folder (overwrite docs/index.html).
5. Keep the restaurant admin/POS screen out of the public Pages root/docs folder if customers must never see it.
6. Test menu loading and submit a test order before sharing the QR link.
