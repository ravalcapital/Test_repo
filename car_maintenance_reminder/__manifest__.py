# -*- coding: utf-8 -*-
{
    'name' : 'Car Maintenance Reminder',
    'version' : '15',
    'category': 'Human Resources/Fleet',
    'summary' : 'Car Maintenance Reminder',
    'depends': [
        'base',
        'fleet',
        'repair',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/maintenance_schedule.xml',
        'views/fleet_vehicle_views.xml',
    ],

    'installable': True,
    'application': True,
}
