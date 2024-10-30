# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Loan Change Terms Installment',
    'version' : '4.1.2',
    'category': 'Accounting/Accounting',
    'depends' : [
        'odoo_customer_supplier_loan',
     ],
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'images': ['static/description/img1.jpg'],
    'price': 129.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': 'Allow to manage Loan Change Terms Installment | Loan Modifications',
    'website': 'www.probuse.com',
    'live_test_url' : 'https://probuseappdemo.com/probuse_apps/loan_change_terms_installment/275',#'https://youtu.be/RY65m1egVoE',
    'description': ''' 
Loan Change Terms Installment
UPDATE Loan Duration (Months)
UPDATE Loan Interest Rate
UPDATE Loan Next Installment Start Date
 ''',
    'data' : [
        'security/ir.model.access.csv',
        'wizard/update_loan_installment_views.xml',
        'views/partner_loan_details_view.xml',
        'views/partner_loan_type_views.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
