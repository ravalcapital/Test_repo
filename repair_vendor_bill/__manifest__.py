# -*- coding: utf-8 -*-
{
    'name': "Repair Vendor Bill",
    'version': '15',
    'summary': """Repair Vendor Bill""",
    'description': """Repair Vendor Bill""",
    'author': "Doaa Khaled",
    'category': 'Repair',
    'depends': ['base','fleet', 'repair' ,'account', 'vehicle_order','crm_quotation_fields', 'mla_module', 'purchase_vehicles', 'hr', 'car_maintenance_reminder'],
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_car_details.xml',
        'views/repair_notify_users.xml',
        'views/repair_car_notify_users.xml',
        'views/repair_order_view.xml',
        'views/account_move.xml',
        'views/fleet_vehicle_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
