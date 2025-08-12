from odoo import models, fields, api


class InheritSaleOrder(models.Model):
    _inherit = "sale.order.line"

    def action_line_button(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Add Product Variants",
            "res_model": "product.variant.wiz",
            "view_mode": "form",
            "view_id": self.env.ref(
                "ti_sale_order.view_product_variant_wizard_form"
            ).id,
            "target": "new",
            "context": {
                "create": False,
                "update": False,
                "default_sale_order_id": self.order_id.id,
                "default_product_id": self.product_id.id,
            },
        }
