{
    "name": "SFTP Workflow Automation",
    "author": "Target Integration",
    "category": "Warehouse Management",
    "version": "18.0.1.0",
    "depends": ["sale"],
    "website": "https://targetintegration.com/",
    "data": [
        "views/popup.xml",
        "views/cron_jobs.xml",
        "security/ir.model.access.csv",
        "views/inherit/sale_view_order_form.xml",
        "views/inherit/res_config_settings_views.xml",
    ],
    "external_dependencies": {
        "python": ["paramiko==4.0.0"],
    },
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
