from pathlib import Path
from odoo import models, fields, api

MODULE_NAME = Path(__file__).parent.parent.name


class InheritSaleOrder(models.Model):
    _inherit = "sale.order"

    send_to_3pl = fields.Boolean("Send to 3PL?")

    def generate_csv_to_3pl(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Something",
            "res_model": "sale.order.3pl.wizard",
            "view_mode": "form",
            # "view_id": self.env.ref(
            #     f"{MODULE_NAME}.view_product_variant_wizard_form"
            # ).id,
            "target": "new",
            "context": {
                "default_sale_order_id": self.id,
            },
        }
