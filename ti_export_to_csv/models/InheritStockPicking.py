from odoo import models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_export_csv(self):
        self.ensure_one()
        if not self.picking_type_id.export_to_csv:
            raise UserError("Export csv not allowed for this picking type")
        return {
            "type": "ir.actions.act_url",
            "url": f"/export/picking/csv/{self.id}",
            "target": "new",
        }
