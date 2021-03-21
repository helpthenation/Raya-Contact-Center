# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LastHeadCount(models.Model):
    _name = 'head.count'
    _description = 'employee_enhancement.employee_enhancement'

    name = fields.Char('Type',required=True)
    description = fields.Text('Notes')


class LastHeadCountLine(models.Model):
    _name = 'head.count.line'
    _description = 'head.count.line'

    _order = "date desc"

    emp_id = fields.Many2one('hr.employee')

    date = fields.Date(required=True)
    head_count_id = fields.Many2one('head.count', string="Head Count Type", required=True)
    description = fields.Text('Notes')

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    #
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
