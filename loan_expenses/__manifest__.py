
{
    'name': 'Loan Expenses',
    'category': 'vehicles',
    'version': '15',
    'summary': """Loan Expenses""",
    'author': 'Doaa Khaled',

    # Dependencies
    'depends': ['account', 'hr_expense', 'odoo_customer_supplier_loan', 'pending_delivery_expenses'],
    # Data
    'data': [
        "views/loan_views.xml",
    ],

    # Technical
    'auto_install': False,
    'installable': True,
    'application': True,
}
