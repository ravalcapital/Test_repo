# -*- coding: utf-8 -*-
{
    'name': "mla_module",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'author': "Christine",
    'website': 'https://www.linkedin.com/in/christine-fayez-018593172',
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/mla_views.xml',
    ],
}
