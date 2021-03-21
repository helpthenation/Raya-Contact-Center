# -*- coding: utf-8 -*-
{
    'name': "wc_ta_extention",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'hr','hr_skills','hr_recruitment','wc_updates','hr_skill_qualification',
    'depends': ['base','hr','hr_skills','mail','hr_recruitment','hr_skill_qualification','employee_enhancement'],
    # 'depends': ['base','wc_hiring_request','wc_sourcing_extension','mail','wc_updates','employee_enhancement'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hiring_request.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
