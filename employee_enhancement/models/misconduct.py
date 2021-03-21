# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Misconduct(models.Model):
    _name = 'employee.misconduct'
    _description = 'employee.misconduct'

    name = fields.Char('Type', required=True)
    applying_restriction = fields.Integer('Applying Restriction')
    description = fields.Text('Notes')



    @api.constrains('applying_restriction')
    def _check_applying_restriction_value(self):
        if self.applying_restriction > 1000 or self.applying_restriction <= 0:
            raise ValidationError(_('Enter Applying Restriction greater than 0.'))


class MisconductLine(models.Model):
    _name = 'employee.misconduct.line'
    _description = 'employee.misconduct.line'

    _order = "date desc"

    emp_id = fields.Many2one('hr.employee')

    date = fields.Date(required=True)
    misconduct_type_id = fields.Many2one('employee.misconduct', string=" Misconduct Type", required=True)
    description = fields.Text('Notes')
