# custom_wanda/__manifest__.py

{
    'name': 'Custom wanda',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Custom Wanda',
    'description': """
        WANDA CUSTOM.
    """,
    'author': 'Wanda Hadis Suara',
    'depends': ['sale', 'purchase', 'web'],
    'data': [
        'views/import_so_lines_wizard.xml',
        'views/sale_order_view.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
