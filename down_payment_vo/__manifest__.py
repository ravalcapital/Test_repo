# -*- coding: utf-8 -*-
{
    'name': "Down Payments VO",
    'description': """
Down Payments VO    """,

    'author': "Christine Fayez",
    'website': "https://www.linkedin.com/in/christine-fayez-018593172",
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['base', 'vehicle_order'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_view.xml',
        'views/vo_view.xml',
    ],

}
