# -*- coding: utf-8 -*-
{
    'name': "gestion_culture",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
     'depends': ['base', 'fleet', 'hr','board'],

    # always loaded
     'data': [
        'security/ir.model.access.csv',
         'data/sequence.xml',
        'views/views.xml',
         'views/fleet.xml',
        'views/templates.xml',
        'views/technicien.xml',
       #  'views/product.xml',
            'views/plante.xml',
          'views/parcelle.xml',
            #  'views/maladie.xml',
        # 'views/dashboard.xml',
      # 'reports/maladie.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
