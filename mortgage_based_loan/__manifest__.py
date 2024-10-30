
{
    'name': 'Mortgage Based Loan',
    'category': 'Loan',
    'version': '15',
    'summary': """Mortgage Based Loan""",
    'author': 'Doaa Khaled',

    # Dependencies
    'depends': ['loan_relation_pending_delivery', 'odoo_customer_supplier_loan'],
    # Data
    'data': [
        "data/loan_type.xml",
        "views/loan_views.xml",
    ],

    # Technical
    'auto_install': False,
    'installable': True,
    'application': True,
}
