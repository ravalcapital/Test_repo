
{
    'name': 'Pending Delivery Expenses',
    'category': 'vehicles',
    'version': '14',
    'summary': """Pending Delivery Expenses""",
    'author': 'Doaa Khaled',

    # Dependencies
    'depends': ['account', 'purchase_vehicles', 'hr_expense'],
    # Data
    'data': [
        "views/pending_delivery_views.xml",
    ],

    # Technical
    'auto_install': False,
    'installable': True,
    'application': True,
}
