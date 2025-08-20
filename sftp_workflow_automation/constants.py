from pathlib import Path

MODULE_NAME = Path(__file__).parent.name
SFTP_HOST_KEY = f"{MODULE_NAME}.sftp_hostname"
SFTP_PORT_KEY = f"{MODULE_NAME}.sftp_port"
SFTP_USERNAME_KEY = f"{MODULE_NAME}.sftp_username"
SFTP_PASSWORD_KEY = f"{MODULE_NAME}.sftp_password"
SFTP_REMOTE_PATH_KEY = f"{MODULE_NAME}.sftp_remote_path"
