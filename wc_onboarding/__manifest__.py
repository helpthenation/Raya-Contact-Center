# -*- coding: utf-8 -*-
{
    'name': "Onboarding",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "White Code",
    'website': "http://www.white-code.co.uk",

    'category': 'Generic module',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base','fetchmail','utm','employee_enhancement','hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/onboarding.xml',
        'views/templates.xml',
        ],

    "installable": True,
    "application": True,
}
