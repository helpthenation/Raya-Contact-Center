# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrApplicant(models.Model):
    _inherit = 'res.partner'

    techskill_ids = fields.One2many(
        'emp.tech.skills', 'applicant_id', 'Technical Skills')
    nontechskill_ids = fields.One2many(
        'emp.nontech.skills', 'applicant_id', 'Non-Technical Skills')
    education_ids = fields.One2many(
        'employee.education', 'applicant_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'applicant_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession', 'applicant_id', 'Professional Experience')
    language_level_ids =  fields.One2many('emp.lang.skills2', 'applicant_id', 'Language Level')

    