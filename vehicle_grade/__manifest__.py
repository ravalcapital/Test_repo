# -*- coding: utf-8 -*-
{
    'name': "Vehicle Grade",
    'version': '15',
    'author': "Doaa Khaled",
    'category': "Fleet",
    'depends': ['base','purchase' , 'fleet', 'purchase_vehicles'],
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_grade_view.xml',
        'views/stock_view.xml',
        'views/purchase_views.xml',
    ],
}

