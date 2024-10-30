# -*- coding: utf-8 -*-
{
    'name': "crm_quotation_fields",

    'author': "Christine",
    'website': "https://www.linkedin.com/in/christine-fayez-018593172",
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'crm_car_details', 'sale_crm', 'vehicle_order'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
