# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Appraisals/Evaluation by HR',
    'version': '2.1.1',
    'price': 99.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Human Resources',
    'summary': 'Periodical Evaluations, Appraisals, Surveys for Employees by HR Department',
    'depends': ['hr', 'calendar', 'survey',],
    'description': """
Appraisals
employee Appraisals
employee Appraisal
Odoo Appraisals
Appraisals
Appraisal
periodical employee evaluation
evaluation process
survey
employee evaluation
hr evaluation
evaluation
evaluation employee
evaluation data
hr evaluation
hr_evaluation
hr job
employee survey
evaluation
employee survey
odoo_hr_evaluation
Appraisals
increment
performance
kpi
employee kpi
employee performance
performance evaluation
evaluation
Employee evaluation
""",
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'http://www.probuse.com',
    'support': 'contact@probuse.com',
    'images': ['static/description/evalu.jpg'],
    # 'live_test_url': 'https://youtu.be/WzUkUXm_KZ0', 
    'live_test_url': 'https://youtu.be/UYjvMCP2Ce4',
    "data": [
        'security/hr_evaluation_security.xml',
        'security/ir.model.access.csv',
        'data/evaluation_mail_template.xml',
        'wizard/next_appraisal_date_view.xml',
        'views/hr_evaluation_view.xml',
        'views/hr_evaluation_installer.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
