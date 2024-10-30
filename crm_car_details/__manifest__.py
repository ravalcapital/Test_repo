# -*- coding: utf-8 -*-
{
    'name': "CRM Car Details",
    'version': '15',
    'author': "Doaa Khaled",
    'category': "CRM",
    'depends': ['crm','car_identity', 'make_model_in_po', 'purchase_vehicles', 'vehicle_order'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/sale_view.xml',
        'views/purchase_views.xml',
        'report/sale_order_report.xml',
    ],
}

