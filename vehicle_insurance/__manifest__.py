# -*- coding: utf-8 -*-

{
    'name': "Vehicle Insurance",

    'summary': """
       Vehicle Insurance""",

    'description': """
        Vehicle Insurance
    """,

    'author': "MHDHELAL",
    'category': 'fleet',
    'version': '15.1',
    'depends': ['base','fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/insurance_groups.xml',
        'wizard/renew_insurance.xml',
        'views/insurance.xml',
        'data/sequence.xml',
        'data/cron.xml',

    ],
}
