import io
import csv
from odoo import http
from pathlib import Path
from odoo.http import request


class Downloader(http.Controller):
    @http.route("/export/picking/csv/<string:filename>", type="http", auth="user")
    def download_picking_csv(self, filename):
        file_loc = f"{Path(__file__).parent.parent}/downloads/{filename}"
        if not Path(file_loc).exists():
            return request.not_found()

        try:
            with open(file_loc, "rb") as f:
                return request.make_response(
                    f.read(),
                    headers=[
                        ("Content-Type", "text/csv"),
                        ("Content-Disposition", f'attachment; filename="{filename}"'),
                    ],
                )

        except Exception as e:
            return request.make_response(
                "something went wrong",
                headers=[("Content-Type", "text/plain")],
                status=500,
            )
        finally:
            if Path(file_loc).exists():
                Path(file_loc).unlink()
