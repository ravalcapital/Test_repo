
{
    'name': "Sale Price Edit Restriction",
    'summary': """
        Restriction to edit Sale Price in sales module""",
    'description': """
        Restriction to edit Sale Price in sales module
    """,
    'author': "Doaa",
    'category': 'Sales',
    'version': '15',

    'depends': ['sale_management'],

    # always loaded
    'data': [
        'security/price_change_security.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
}
