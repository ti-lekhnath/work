from odoo import models, fields


class InheritPickingType(models.Model):
    _inherit = "stock.picking.type"

    export_to_csv = fields.Boolean(string="Export to csv")
