# -*- coding: utf-8 -*-
{
    'name': "Pending Delivery Vendor Bill",
    'version': '15',
    'summary': """Pending Delivery Vendor Bill""",
    'description': """Pending Delivery Vendor Bill""",
    'author': "Doaa Khaled",
    'category': 'Purchase',
    'depends': ['base', 'account', 'purchase', 'purchase_vehicles'],
    'data': [
        'views/ir_config_setting.xml',
        'views/product_views.xml',
        'views/pending_delivery_view.xml',
        'views/account_move.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
