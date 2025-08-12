from odoo import models, fields, api


class ProductVariantLine(models.TransientModel):
    _name = "product.variant.line"

    wizard_id = fields.Many2one("product.variant.wiz")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    product_variant_id = fields.Many2one("product.product", string="Product Variant")
    quantity = fields.Float(string="Quantity", default=0.0)
