# -*- coding: utf-8 -*-
{
    'name': "production",

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
   'depends': ['base','product','reproduction','sale',
'gestion_culture'],

    # always loaded
    'data': [
       #  'security/ir.model.access.csv',
           'data/data.xml',
           'views/views.xml',
           'views/templates.xml',
           'views/listes.xml',
           'views/stock.xml',
           'views/client.xml',
           'views/tec.xml',
           'views/mvt.xml',
                'views/stockplan.xml',
         'views/Taches.xml',
      
           #     'views/listeplanif.xml',
        #    'views/planification.xml',
             'views/productlist.xml',
          #  'views/production.xml',
        #   'views/kanban.xml',
       
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

