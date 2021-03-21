# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EmployeeGrade(models.Model):
    _name = 'employee.grade'
    _description = 'employee_grade'

    name = fields.Char()
    garde = fields.Integer(required=True)
    description = fields.Text('Notes')
    grade_level_exception = fields.Integer(default="1")

    # value2 = fields.Float(compute="_value_pc", store=True)



    @api.constrains('garde','grade_level_exception')
    def _check_grade_value(self):
        if self.garde > 1000 or self.garde <= 0:
            raise ValidationError(_('Enter Grade greater than 0.'))
        if self.grade_level_exception > 1000 or self.grade_level_exception <= 0:
            raise ValidationError(_('Enter Grade Level Exception greater than 0.'))
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
