# -*- coding: utf-8 -*-
{
    'name': "Sale Order Approval",

    'summary': """Sale Order Approval""",

    'author': "Doaa Khaled",
    'E-mail': "doaakhaled6969@gmail.com",
    'category': 'sale',
    'version': '13',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'wizards/sale_view.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
