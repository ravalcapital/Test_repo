# -*- coding: utf-8 -*-
{
    'name': "Rental Calculations",

    'author': "Christine Fayez",
    'website': "https://www.linkedin.com/in/christine-fayez-018593172",
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_crm', 'crm_car_details'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
