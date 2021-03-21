# -*- coding: utf-8 -*-
{
    'name': "Raya Refuse",

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
    'depends': ['base','hr_recruitment','wc_hiring_request','wc_ta_extention','wc_raya_quality'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/applicant.xml',
    ],
}
