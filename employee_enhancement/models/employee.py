# -*- coding: utf-8 -*-

from odoo import models, fields, api


class employee_enhancement(models.Model):
    _inherit = 'hr.employee'

    employee_grade = fields.Many2one('employee.grade',related="job_id.employee_grade")

    head_count_dates_ids = fields.One2many('head.count.line','emp_id')
    misconduct_ids = fields.One2many('employee.misconduct.line','emp_id')

    # name = fields.Char()
    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()
    #
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100


class employee_enhancement_job(models.Model):
    _inherit = 'hr.job'

    employee_grade = fields.Many2one('employee.grade')
    head_count_restriction = fields.Integer('Head Count Restriction', default="6")
    job_category = fields.Selection([('talent','Talent Aqcusiotion'),('operational','Operational')],string="Job Category")
