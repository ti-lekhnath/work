from odoo import models, fields
from ..constants import (
    SFTP_HOST_KEY,
    SFTP_PORT_KEY,
    SFTP_USERNAME_KEY,
    SFTP_PASSWORD_KEY,
    SFTP_REMOTE_PATH_KEY,
)



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
        params.set_param(SFTP_HOST_KEY, self.sftp_hostname or "")
        params.set_param(SFTP_PORT_KEY, self.sftp_port or 22)
        params.set_param(SFTP_USERNAME_KEY, self.sftp_username or "")
        params.set_param(SFTP_PASSWORD_KEY, self.sftp_password or "")
        params.set_param(SFTP_REMOTE_PATH_KEY, self.sftp_remote_path or "")

    def get_values(self):
        res = super().get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            sftp_hostname=params.get_param(SFTP_HOST_KEY, ""),
            sftp_port=int(params.get_param(SFTP_PORT_KEY, 22)),
            sftp_username=params.get_param(SFTP_USERNAME_KEY, ""),
            sftp_password=params.get_param(SFTP_PASSWORD_KEY, ""),
            sftp_remote_path=params.get_param(SFTP_REMOTE_PATH_KEY, ""),
        )
        return res
