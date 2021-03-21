# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ApplicantGetRefuseReason(models.TransientModel):
    _name = 'applicant.get.transfer.reason'
    _description = 'Transfer Application'

    job_id = fields.Many2one('hr.job','Select a Job ')
    applicant_ids = fields.Many2many('hr.applicant')

    def action_transfer_reason_apply(self):
        return self.applicant_ids.write({'job_id': self.job_id.id})