# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
class PositionHold(models.Model):
    _inherit = "hr.job"
    quality_hold = fields.Boolean()
class ApplicantRefuseReason(models.Model):
    _inherit = "hr.applicant"
    quality_hold= fields.Boolean('Quality Hold', default=False, track_visibility="onchange")
    def quality_hold_release(self):
        self.quality_hold=False
    @api.onchange('emp_id','job_id')
    def check_quality_hold(self):
         for this in self:
             print("###################################################")
             print(this)
             print(this.job_id)
             print(this.job_id.quality_hold)
             print(this.emp_id)
             print("###################################################")
             if this.job_id and this.job_id.quality_hold and this.emp_id:
                 this.quality_hold=True

    @api.onchange('stage_id')
    def check_stage_hold(self):
        if self.quality_hold==True:
            raise ValidationError('This applicant currently on Quality Hold')
