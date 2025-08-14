import copy
from odoo import models, fields, api


class ProductVariantWiz(models.TransientModel):
    _name = "product.variant.wiz"
    _description = "Wizard for adding variants to sale order line"

    sale_order_id = fields.Many2one("sale.order")
    product_id = fields.Many2one("product.product")
    variant_line_ids = fields.One2many("product.variant.line", "wizard_id")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        sale_order_id = self._context.get("default_sale_order_id")
        product = self.env["product.product"].browse(
            self._context.get("default_product_id")
        )

        if not product:
            return res

        variants = self.env["product.product"].search(
            [("product_tmpl_id", "=", product.product_tmpl_id.id)]
        )

        product_quantity_map = {}
        for line in self.env["sale.order.line"].search(
            [("order_id", "=", sale_order_id)]
        ):
            if line.product_id.id not in product_quantity_map:
                product_quantity_map[line.product_id.id] = []
            product_quantity_map[line.product_id.id].append(
                (line, line.product_uom_qty)
            )

        variant_lines = []
        for variant in variants:
            defaults = {
                "quantity": 0,
                "sale_order_line_id": False,
                "product_variant_id": variant.id,
            }

            if variant.id not in product_quantity_map:
                variant_lines.append((0, 0, defaults))
                continue
            for order_line, quantity in product_quantity_map.get(variant.id, []):
                defaults["sale_order_line_id"] = order_line.id
                defaults["quantity"] = quantity
                variant_lines.append((0, 0, copy.deepcopy(defaults)))

        res["variant_line_ids"] = variant_lines
        return res

    def action_confirm(self):
        sale_order = self.sale_order_id

        for line in self.variant_line_ids:
            if line.sale_order_line_id and line.quantity <= 0:
                line.sale_order_line_id.unlink()
            elif line.sale_order_line_id and line.quantity > 0:
                line.sale_order_line_id.write(
                    {
                        "product_uom_qty": line.quantity,
                        "product_uom": line.product_variant_id.uom_id.id,
                    }
                )
            elif not line.sale_order_line_id and line.quantity > 0:
                self.env["sale.order.line"].create(
                    {
                        "order_id": sale_order.id,
                        "product_id": line.product_variant_id.id,
                        "product_uom_qty": line.quantity,
                        "product_uom": line.product_variant_id.uom_id.id,
                    }
                )
