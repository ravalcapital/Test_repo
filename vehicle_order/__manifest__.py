# -*- coding: utf-8 -*-
{
    'name': "Vehicle Order",

    'description': """
Vehicle Order    """,
    'author': "Christine Fayez",
    'website': "https://www.linkedin.com/in/christine-fayez-018593172",
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['mla_module', 'fleet', 'sale', 'account', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/views.xml',
        'data/vo_seq.xml',
        'reports/vo_reports.xml',
        'reports/bank_details.xml',
        'reports/report_vehicle_order_invoice.xml',
        'views/bank_details.xml',
        'views/account_move.xml',
        'views/product_views.xml',
        'views/mla_views.xml',
    ],

}
