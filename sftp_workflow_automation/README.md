# ti_saequip_export_sale_order_3pl

## Summary
- Added a checkbox **Send to 3PL?** on Sale Orders to control CSV export availability.
- Created a button **Generate CSV for 3PL** on Sale Orders to generate a CSV for selected records.
- Implemented CSV download containing Sale Order and Sale Order Line fields as selected by the user.
- Generated CSV is attached to the Sale Order chatter for reference.
- Added SFTP integration to automatically upload CSV files to the configured remote path.
- Configurable SFTP credentials and path from the Settings page.
- Hourly scheduled action to scan and upload previously generated CSV files, deleting local copies after successful upload.

## Demo
Click [here](https://portal07.sharepoint.com/:v:/s/OdooDevs/EQoaYuEhhDZAvwIT1Q42VmEBZB3H7s-qeadOHtd3CqecmQ?e=k2iiy8) to watch the demo.

## Ticket
You can track the task [here](https://mypmstudio.com/issues/71581).
