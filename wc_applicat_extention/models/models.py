from odoo import fields, models, api, _


class HRJOB(models.Model):
    _inherit = 'hr.job'
    prooject = fields.Many2one('rcc.project',string="Project")