# -*- coding: utf-8 -*-
{
    'name' : 'Fleet Odometer',
    'version' : '15',
    'category': 'Human Resources/Fleet',
    'summary' : 'Manage your fleet and track car costs',
    'depends': [
        'base',
        'fleet',
        'hr',
        'vehicle_order',
        'stock',
        'crm_quotation_fields'
    ],
    'data': [
        'security/fleet_security.xml',
        'security/ir.model.access.csv',
        'views/stock_view.xml',
        'views/fleet_cars_odometer.xml',
        'views/vehicle_order.xml',
    ],


    'installable': True,
    'application': True,
}
