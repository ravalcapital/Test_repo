# -*- coding: utf-8 -*-

{
    'name': "Vehicle License",
    'description': "Vehicle License",
    'author': "Doaa",
    'category': 'Fleet',
    'version': '15',
    'depends': ['base','fleet', 'purchase_vehicles'],
    'data': [
        'security/ir.model.access.csv',
        'views/license.xml',
        'views/pending_delivery_views.xml',
        'views/sequence.xml',
    ],
}
