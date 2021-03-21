# -*- coding: utf-8 -*-
{
    'name': 'wc Screening Excel',
    'version': '14.0',
    'category': 'Generic module',
    'description': """
        Long description of module's purpose
    """,
    'author': "White Code",
    'depends': ['hr_recruitment','hr', 'hr_skill_qualification', 'wc_hiring_request'],
    'data': [
       'security/ir.model.access.csv',
       'views/screening_excel.xml'
    ],
    'installable': True,
    'application': True,
}
