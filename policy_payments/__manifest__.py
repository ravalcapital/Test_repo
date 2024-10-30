
{
    'name': 'Policy Payments',
    'category': 'vehicles',
    'version': '15',
    'summary': """Policy Payments""",
    'author': 'Doaa Khaled',

    # Dependencies
    'depends': ['account', 'purchase_vehicles'],
    # Data
    'data': [
        "security/ir.model.access.csv",
        "views/pending_delivery_views.xml",
        "wizard/pending_delivery_payment_wizard.xml",
    ],

    # Technical
    'auto_install': False,
    'installable': True,
    'application': True,
}
