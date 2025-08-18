from odoo import models, fields, api


class InheritSaleOrder(models.Model):
    _inherit = "sale.order"

    def generate_csv_to_3pl(self):
        print("Button clicked in Sale Order Line")
