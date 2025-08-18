import os
import io
import csv
from pathlib import Path
from datetime import datetime
from odoo import models, _
from odoo.exceptions import UserError
from odoo.http import request


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _csv_type_label(self):
        if self.picking_type_code == "incoming":
            return "Putaway"
        if self.picking_type_code in ("mrp_operation"):
            return "PICK"
        return self.picking_type_code or "Unknown"

    def action_export_to_csv(self):
        download_at = f"{Path(__file__).parent.parent}/downloads"
        os.makedirs(download_at, exist_ok=True)

        if not self:
            raise UserError(_("No records selected."))

        for picking in self:
            if not picking.picking_type_id.export_to_csv:
                raise UserError(
                    _("Export To CSV is not enabled for operation type: %s")
                    % picking.picking_type_id.display_name
                )

        filename = f"pick_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(download_at, filename)

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Order", "Type", "Item", "Quantity", "LotNumber"])

            for picking in self:
                for move_line in picking.move_line_ids:
                    writer.writerow(
                        [
                            picking.name,
                            picking._csv_type_label(),
                            move_line.product_id.default_code or "",
                            move_line.quantity,
                            move_line.lot_id.name or "",
                        ]
                    )

        return {
            "type": "ir.actions.act_url",
            "url": f"/export/picking/csv/{filename}",
            "target": "new",
        }
