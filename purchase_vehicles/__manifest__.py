
{
    'name': 'Purchase Vehicles',
    'category': 'vehicles',
    'version': '14',
    'summary': """Purchase Vehicles Management""",
    'author': 'Doaa Khaled',

    # Dependencies
    'depends': ['fleet', 'sale_management', 'stock', 'purchase', 'purchase_stock', 'make_model_in_po', 'analytic', 'vehicle_insurance','crm'],
    # Data
    'data': [
        "security/ir.model.access.csv",
        "security/security.xml",
        "security/ir_rule.xml",
        "views/pending_delivery_view.xml",
        "views/product_views.xml",
        "views/purchase_order_view.xml",
        "views/stock_view.xml",
        "views/vehicle_insurance_view.xml",
        "views/crm_car_color.xml",
    ],

    # Technical
    'auto_install': False,
    'installable': True,
    'application': True,
}
