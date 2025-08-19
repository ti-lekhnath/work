import os
import csv
import base64
from pathlib import Path
from odoo import models, fields


class SaleOrder3PLWizard(models.TransientModel):
    _name = "sale.order.3pl.wizard"
    _description = "Wizard to select fields for 3PL CSV"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", required=True, store=False
    )

    sale_order_field_ids = fields.Many2many(
        "ir.model.fields",
        relation="sale_order_wizard_field_rel",
        column1="wizard_id",
        column2="field_id",
        string="Sale Order Fields",
        domain=[("model", "=", "sale.order")],
    )

    sale_order_line_field_ids = fields.Many2many(
        "ir.model.fields",
        relation="sale_order_line_wizard_field_rel",
        column1="wizard_id",
        column2="field_id",
        string="Sale Order Line Fields",
        domain=[("model", "=", "sale.order.line")],
    )

    # def action_generate_csv(self):
    #     """Generate CSV with selected fields"""
    #     active_id = self.env.context.get("active_id")
    #     sale_order = self.env["sale.order"].browse(active_id)

    #     headers = []
    #     row = []

    #     # Add sale order fields
    #     for field in self.sale_order_field_ids:
    #         headers.append(field.field_description)
    #         row.append(getattr(sale_order, field.name, ""))

    #     # Add sale order line fields
    #     for line in sale_order.order_line:
    #         for field in self.sale_order_line_field_ids:
    #             headers.append(field.field_description)
    #             row.append(getattr(line, field.name, ""))

    #     # Build CSV content
    #     import io, csv, base64

    #     buffer = io.StringIO()
    #     writer = csv.writer(buffer)
    #     writer.writerow(headers)
    #     writer.writerow(row)

    #     # Create attachment so user can download
    #     attachment = self.env["ir.attachment"].create(
    #         {
    #             "name": f"3PL_{sale_order.name}.csv",
    #             "type": "binary",
    #             "datas": base64.b64encode(buffer.getvalue().encode()),
    #             "res_model": "sale.order",
    #             "res_id": sale_order.id,
    #             "mimetype": "text/csv",
    #         }
    #     )

    #     return {
    #         "type": "ir.actions.act_url",
    #         "url": f"/web/content/{attachment.id}?download=true",
    #         "target": "self",
    #     }

    def action_generate_csv(self):
        self.ensure_one()
        sale_order = self.env["sale.order"].browse(self.sale_order_id.id)
        sale_order_fields = [field.name for field in self.sale_order_field_ids]
        sale_order_line_fields = [field.name for field in self.sale_order_line_field_ids]

        file_path = f"{Path(__file__).parent}/test.csv"
        get_data = lambda record, fields: [getattr(record, field, "") for field in fields]
        with open(file_path, mode="w", newline="") as buffer:
            writer = csv.writer(buffer)
            writer.writerow(sale_order_fields + sale_order_line_fields)

            for line in sale_order.order_line:
                row = get_data(sale_order, sale_order_fields) + get_data(line, sale_order_line_fields)
                writer.writerow(row)


        attachment = self.env["ir.attachment"].create({
            "name": f"sale_order_{sale_order.name}.csv",
            "res_model": "sale.order",
            "res_id": sale_order.id,
            "type": "binary",
            "datas": base64.b64encode(open(file_path, "rb").read()),
            "mimetype": "text/csv",
        })


        sale_order.message_post(
            body="CSV file generated and attached.",
            attachment_ids=[attachment.id],
        )

        return {"type": "ir.actions.act_window_close"}
