# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError


class wc_interview_checklist(models.Model):
    _name = 'wc_interview_checklist.wc_interview_checklist'
    _description = 'Interview Checklist'

    name = fields.Char()
    check = fields.Boolean()

class wc_interview_checklist_applicant(models.Model):
    _name = 'wc_interview_checklist_applicant'
    _description = 'Interview Checklist Applicant'

    name = fields.Char()
    check = fields.Boolean()
    note = fields.Char()
    applicant_id = fields.Many2one('hr.applicant')

class HrJob(models.Model):
    _inherit = 'hr.job'

    interview_check = fields.Boolean('Interview Checklist')
    interview_checklist = fields.Many2many('wc_interview_checklist.wc_interview_checklist','interview_checklist_job_rel','job_id','check_id')

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    interview_check = fields.Boolean('Interview Question', related="job_id.interview_check")
    interview_checklist = fields.One2many('wc_interview_checklist_applicant','applicant_id')
    interview_checklist_checkbox = fields.Boolean(compute="_compute_interview_checklist_checkbox")
    @api.onchange('stage_id')
    def _compute_interview_checklist_checkbox(self):
        for this in self:
            if this.stage_id.interview_checklist_checkbox:
                this.interview_checklist_checkbox = True
            else:
                this.interview_checklist_checkbox = False
    def read(self, fields=None, load='_classic_read'):
        res = super(HrApplicant, self).read(fields, load)
        for this in self:
            if this.interview_checklist_checkbox:
                job_ids = self.env['hr.job'].search([('id','=',this.job_id.id)],limit=1)
                lines = []
                if len(this.interview_checklist)>0:
                    pass
                else:
                    for line in job_ids.interview_checklist:
                        vals = (0, 0, {
                        'name': line.name,
                        'check': line.check,
                        'applicant_id':this.id
                        })
                        lines.append(vals)
                    this.interview_checklist=lines
        return res



class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    interview_checklist_checkbox = fields.Boolean()
