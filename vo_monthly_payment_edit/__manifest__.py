# -*- coding: utf-8 -*-
{
    'name': "vo_monthly_payment_edit",
    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'depends': ['vehicle_order','fleet_odometer'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/fleet_vehicle.xml',

    ],

}
