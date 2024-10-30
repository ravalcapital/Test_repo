{
    'name': "Operation Forms",
    'description': """
Operation Forms    """,
    'author': "Christine Fayez",
    'website': "https://www.linkedin.com/in/christine-fayez-018593172",
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['stock', 'mla_module', 'vehicle_order', 'rfq_vo', 'mla_order_relations', 'crm_quotation_fields','vo_monthly_payment_edit'],
    'data': [
        'security/operation_security.xml',
        'security/ir.model.access.csv',
        'data/args_seq.xml',
        'data/paper_format.xml',
        # views
        'views/base_view.xml',
        'views/vehicle_views.xml',
        'views/views.xml',

        # reports
        'reports/layout.xml',
        'reports/car_rental_base_template.xml',
        'reports/car_rental_agreement.xml',
        'reports/outsource.xml',
        'reports/short_term.xml',
        'reports/prelease.xml',
        'reports/replacement.xml',
        'reports/non_replace.xml',
        'reports/anex_report.xml'

    ],
    'license': 'LGPL-3',

}
