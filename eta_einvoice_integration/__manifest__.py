# -*- coding: utf-8 -*-
{
    'name': "E-Invoice Integration",
    'summary': """
            Egyptian Tax Authority Invoice Integration
        """,
    'description': """
       This module integrate with the ETA Portal to automatically sign and send your invoices to the tax Authority.
    """,
    'author': 'Plementus',
    'website': 'https://www.plementus.com',

    'contributors': [
        'Mario Roshdy <marioroshdyn@gmail.com>',
        'Karim Jaber <kareem@plementus.com>'
    ],
    'category': 'account',
    'version': '0.1',
    'depends': ['base', 'account', 'stock', 'sale'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/account_tax_view.xml',
        'views/product_template_view.xml',
        'views/res_company_view.xml',
        'views/res_config_settings_view.xml',
        'views/res_partner_view.xml',
        'views/uom_uom_view.xml',
        'views/account_move_view.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'eta_einvoice_integration/static/src/js/sigin_invoice.js',
        ],
    },

}
