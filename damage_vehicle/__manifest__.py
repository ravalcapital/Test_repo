# -*- coding: utf-8 -*-
{
    'name' : 'Damage Vehicle',
    'version' : '15',
    'category': 'Human Resources/Fleet',
    'depends': [
        'base',
        'fleet',
        'vehicle_order',
        'mla_module',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/damage_vehicle_view.xml',
        'views/product_views.xml',
    ],


    'installable': True,
    'application': True,
}
