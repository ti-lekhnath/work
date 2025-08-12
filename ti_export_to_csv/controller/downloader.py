import io
import csv
from odoo import http
from odoo.http import request


class Downloader(http.Controller):
    @http.route("/export/picking/csv/<int:_id>", type="http", auth="user")
    def download_picking_csv(self, _id):
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Order", "Item", "Demand", "Done"])

        for picking in request.env["stock.picking"].browse(_id):
            for move in picking.move_ids_without_package:
                writer.writerow(
                    [
                        picking.name,
                        move.product_id.default_code or "",
                        move.product_uom_qty,
                        move.quantity,
                    ]
                )

        buffer.seek(0)
        content = buffer.read()
        buffer.close()

        return request.make_response(
            content,
            headers=[
                ("Content-Type", "text/csv"),
                (
                    "Content-Disposition",
                    f'attachment; filename="picking_{picking.name}.csv"',
                ),
            ],
        )
