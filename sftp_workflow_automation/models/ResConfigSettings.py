# my_module/models/res_config_settings.py
from odoo import models, fields
from pathlib import Path


MODULE_NAME = Path(__file__).parent.parent.name

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sftp_hostname = fields.Char("SFTP Hostname")
    sftp_port = fields.Integer("SFTP Port", default=22)
    sftp_username = fields.Char("SFTP Username")
    sftp_password = fields.Char("SFTP Password")
    sftp_remote_path = fields.Char("Remote Upload Path")

    def set_values(self):
        super().set_values()
        params = self.env["ir.config_parameter"].sudo()
        params.set_param(f"{MODULE_NAME}.sftp_hostname", self.sftp_hostname or "")
        params.set_param(f"{MODULE_NAME}.sftp_port", self.sftp_port or 22)
        params.set_param(f"{MODULE_NAME}.sftp_username", self.sftp_username or "")
        params.set_param(f"{MODULE_NAME}.sftp_password", self.sftp_password or "")
        params.set_param(f"{MODULE_NAME}.sftp_remote_path", self.sftp_remote_path or "")

    def get_values(self):
        res = super().get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            sftp_hostname=params.get_param(f"{MODULE_NAME}.sftp_hostname", ""),
            sftp_port=int(params.get_param(f"{MODULE_NAME}.sftp_port", 22)),
            sftp_username=params.get_param(f"{MODULE_NAME}.sftp_username", ""),
            sftp_password=params.get_param(f"{MODULE_NAME}.sftp_password", ""),
            sftp_remote_path=params.get_param(f"{MODULE_NAME}.sftp_remote_path", ""),
        )
        return res
