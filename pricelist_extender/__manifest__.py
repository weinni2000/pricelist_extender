{
    'name': 'Pricelist Category and recommended price',
    'summary': """
        Tools extending the Price List Template to incluede the List Price and to organise the Products in Kategories
        """,

    'description': """
        Tools extending the Price List Template to incluede the List Price and to organise the Products in Kategories
    """,
    'license': 'OPL-1',
    'author': "mytime.click",
    'website': "https://www.mytime.click",
    'version': '15.0.1.0.0',
    'depends': ["base", "product", "website", "sale"],
    'data': [
        'reports/pricelist_extender.xml',
        'views/settings.xml',
        'data/res_config_data.xml',
        'security/ir.model.access.csv',
        'security/multicompany.xml',
        'views/product_season_view.xml',
        'views/product_template_view.xml',
        'views/product_category_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
