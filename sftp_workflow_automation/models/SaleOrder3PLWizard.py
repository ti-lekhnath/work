import os
import csv
import base64
import paramiko
from pathlib import Path
from odoo import models, fields

from ..constants import (
    SFTP_HOST_KEY,
    SFTP_PORT_KEY,
    SFTP_USERNAME_KEY,
    SFTP_PASSWORD_KEY,
    SFTP_REMOTE_PATH_KEY,
)


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
        default=lambda self: self.get_sale_order_field_defaults(),
    )

    sale_order_line_field_ids = fields.Many2many(
        "ir.model.fields",
        relation="sale_order_line_wizard_field_rel",
        column1="wizard_id",
        column2="field_id",
        string="Sale Order Line Fields",
        domain=[("model", "=", "sale.order.line")],
        default=lambda self: self.get_sale_order_line_field_defaults(),
    )

    def get_sale_order_line_field_defaults(self):
        fields = ["product_id", "product_uom_qty", "price_unit", "price_total"]
        return self.env["ir.model.fields"].search(
            [("model", "=", "sale.order.line"), ("name", "in", fields)]
        )

    def get_sale_order_field_defaults(self):
        fields = ["client_order_ref", "display_name", "partner_id"]
        return self.env["ir.model.fields"].search(
            [("model", "=", "sale.order"), ("name", "in", fields)]
        )

    def file_upload(self):
        conf = self.env["ir.config_parameter"].sudo()
        host = conf.get_param(SFTP_HOST_KEY)
        port = int(conf.get_param(SFTP_PORT_KEY))
        username = conf.get_param(SFTP_USERNAME_KEY)
        password = conf.get_param(SFTP_PASSWORD_KEY)
        remote_path = conf.get_param(SFTP_REMOTE_PATH_KEY)

        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(f"{Path(__file__).parent}/test.csv", f"{remote_path}/test.csv")

    def action_generate_csv(self):
        self.ensure_one()
        sale_order = self.env["sale.order"].browse(self.sale_order_id.id)
        sale_order_fields = [field.name for field in self.sale_order_field_ids]
        sale_order_line_fields = [
            field.name for field in self.sale_order_line_field_ids
        ]

        file_path = f"{Path(__file__).parent}/test.csv"
        get_data = lambda record, fields: [
            getattr(record, field, "") for field in fields
        ]
        with open(file_path, mode="w", newline="") as buffer:
            writer = csv.writer(buffer)
            writer.writerow(sale_order_fields + sale_order_line_fields)

            for line in sale_order.order_line:
                row = get_data(sale_order, sale_order_fields) + get_data(
                    line, sale_order_line_fields
                )
                writer.writerow(row)

        attachment = self.env["ir.attachment"].create(
            {
                "name": f"sale_order_{sale_order.name}.csv",
                "res_model": "sale.order",
                "res_id": sale_order.id,
                "type": "binary",
                "datas": base64.b64encode(open(file_path, "rb").read()),
                "mimetype": "text/csv",
            }
        )

        sale_order.message_post(
            body="#PL CSV File",
            attachment_ids=[attachment.id],
        )

        self.file_upload()

        return {"type": "ir.actions.act_window_close"}
