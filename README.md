# Fieldcard — MAO Baggao Farmer ID Generator

A fully static, offline-ready app. Open **index.html** in a modern browser. No installation, server, database, external fonts, or CDN required. It can also be hosted on any static web host.

## Use
1. Download the CSV template using the app. Export your RSBSA list as a UTF-8, comma-separated CSV.
2. Import CSV and match columns. RSBSA number and full name (or first and last name) are required. Incomplete records are skipped. Rows with the same RSBSA number are combined into one farmer, merging only the commodities present in those rows. Basic details use the first valid row. Imports replace the current list.
3. Open Settings to upload the official office logo, edit the office/locality, and set the signatory.
4. Select a farmer to view the ID. Add an optional photo per farmer for this session.
5. Print one ID or all filtered IDs. Each farmer's front and back appear together on A4. Cut and mount the two sides together. Use 100% / actual-size printing, enable background graphics, and disable browser headers/footers. Test one ID before a full batch. Final card dimensions target 85.6 × 54 mm; browser printer settings can affect scaling.

6. Click **Save as images** for the selected farmer. Download the front and back separately from the dialog as 1440 × 908 pixel PNG files. Both sides render regardless of the currently visible preview side. Export is entirely local and works offline.

## Data and limitations
- QR payload is the exact imported RSBSA number, not a verification link. Scan using a camera/QR reader. It does not check registration against any government system.
- Preserve RSBSA numbers as text in spreadsheets to keep leading zeros. CSV cannot recover zeros already removed by Excel.
- Basic fields: name, RSBSA number, barangay, municipality, province, sex, birth date, and commodity/livelihood. Blank municipality/province default to Baggao/Cagayan.
- CSV supports quoted commas, escaped quotes, multiline fields and UTF-8 BOM. It does not support semicolon delimiters or XLSX files.
- Farmer data/photos remain in memory only and disappear on reload. Office settings/logo use browser local storage when available. Clear data removes the current records and generated print markup. Do not use a shared browser profile for confidential settings.
- Uploaded images are resized locally. A photo is optional; adding photos is manual, not imported from CSV.
- This is a local template, not an officially approved government ID. Confirm branding, layout and personal data handling with the office before issuing. Very long names/addresses can be clipped; inspect previews.
- Demo records are fictional and marked as samples.

QR generation library: QRCode.js by David Shim (MIT), bundled inside index.html. No network calls are required.

Image export: html2canvas 1.4.1 (MIT), bundled inside index.html.

## Multiple commodities
Click **Edit commodities** for the selected farmer. Select Rice, Corn, Vegetables, and/or enter other commodities. The ID displays the selected crops; changes last for the current session.
In CSV, use a quoted value such as `"Rice, Corn"` in the Commodity column, or `Rice; Corn` / `Rice|Corn`. Duplicate values are removed. Inspect the preview if a farmer has many crops, since card space is limited.

The front footer now reads: THIS WILL SERVE AS YOUR VALID ID WHEN TRANSACTING TO MAO-BAGGAO,CAGAYAN. This wording is user-configured; office approval is still required before issuance. Demo farmers remain marked DEMO in the farmer heading.

## Crop rows grouped by farmer
The import does not assume a farmer grows both Rice and Corn. It groups rows by exact RSBSA number and combines the commodities actually provided:
- Rice row only → Rice
- Corn row only → Corn
- Rice row + Corn row with the same RSBSA number → Rice, Corn
- Empty commodity → no crop displayed

Example:
```csv
RSBSA Number,Full Name,Barangay,Commodity
0001,Juan Dela Cruz,Sample Barangay,Rice
0001,Juan Dela Cruz,Sample Barangay,Corn
0002,Maria Santos,Sample Barangay,Rice
0003,Pedro Reyes,Sample Barangay,Corn
```
This produces three IDs: Juan with Rice and Corn, Maria with Rice, and Pedro with Corn. There is no automatic crop assignment. Manual commodity edits remain available; only use them to correct verified records.

## PWA installation and deployment
This app is now a Progressive Web App (PWA). Upload all files from the ZIP, keeping them together, to a static **HTTPS** host. No backend is needed. Do not host only index.html: the manifest, service worker, and icons are required. The host must serve sw.js as JavaScript and must not redirect it to HTML. A dedicated directory/subdomain is recommended.

1. Visit the hosted app online once and wait for the offline-ready message.
2. Chrome/Edge (Android or desktop): use **Install app** when shown, or the browser's Install app menu.
3. iPhone/iPad: open the HTTPS URL in Safari, then Share → Add to Home Screen.
4. Launch the installed app. The interface, QR codes, CSV imports, printing, and image generation work offline after caching. Download and printing capabilities depend on the device/browser.

Opening index.html directly still works as a standalone static app, but file:// cannot install or cache a PWA. Local development can use http://localhost. The in-app file preview is not a PWA host.

The PWA caches the app files only, not farmer records. Farmer records/photos are still session-only: closing/reloading the app clears them. Installation does not create a farmer database. Office settings/logo remain in local browser storage and are specific to that host/browser.

For updates, deploy the updated files and bump CACHE in sw.js (e.g. fieldcard-pwa-v2). Revisit online, then close all app windows and reopen when prompted. Clear site data/unregister the service worker to completely remove cached app files and settings.

Files: index.html, manifest.webmanifest, sw.js, icon-192.png, icon-512.png, README.md.
