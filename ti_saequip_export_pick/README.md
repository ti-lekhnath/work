# ti_saequip_export_pick

## Summary
- Added a checkbox **Export To CSV?** on operation types to control CSV export availability.
- Created a **server action** "Export To CSV" on transfers to generate a CSV file for selected records.
- Implemented CSV download containing: Order, Type, Item, Quantity, and Lot/Serial Number.
- Enabled bulk export of multiple transfers into a single CSV file.
- Added HTTP route to serve the generated CSV for download.
