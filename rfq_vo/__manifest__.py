# -*- coding: utf-8 -*-
{
    'name': "RFQ From Vehicle Order",

    'description': """
RFQ From Vehicle Order    """,

    'author': "Christine Fayez",
    'website': "https://www.linkedin.com/in/christine-fayez-018593172",
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['base', 'vehicle_order', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/purchase.xml'
    ],

}
