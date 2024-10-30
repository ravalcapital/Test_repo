# -*- coding: utf-8 -*-
{
    'name' : 'Car Identity',
    'version' : '15',
    'category': 'Human Resources/Fleet',
    'depends': [
        'base',
        'fleet',
        'stock',
        'vehicle_order',
        'sale',
        'purchase',
        'purchase_vehicles',
        'vehicle_grade'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/car_identity_view.xml',
        'views/product_views.xml',
        'views/lot_serial_view.xml',
        'views/fleet_vehicle_views.xml',
        'views/pending_delivery_views.xml',
        'views/purchase_views.xml',
        'views/sale_view.xml',
        'views/stock_view.xml',
    ],


    'installable': True,
    'application': True,
}
