# -*- coding: utf-8 -*-
{
    'name': "WC CZ Integration",

    'summary': """
        Integration Between Odoo and Connect Zone HR System. """,

    'description': """
     Integration Between Odoo and Connect Zone HR System.
    """,

    'author': "White Code Co",
    'website': "http://www.white-code.co.uk",

    'category': 'Generic module',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base','employee_enhancement','hr'],

    # always loaded
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
       #'views/views.xml',
        #'views/templates.xml',
        ],

    "installable": True,
    "application": True,
}
