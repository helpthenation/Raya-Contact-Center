# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ApplicantLostReason(models.TransientModel):
    _name = 'applicant.lost.interest.reason'
    _description = 'Get Interest Losing Reason'

    interest_reason_id = fields.Many2one('hr.applicant.lost.interest.reason', 'Lost Interest Reason')
    applicant_ids = fields.Many2many('hr.applicant')

    def action_lost_interest_apply(self):
        return self.applicant_ids.write({'interest_reason_id': self.interest_reason_id.id, 'active': False})

class LostInterestName(models.Model):
    _name = 'hr.applicant.lost.interest.reason'

    name = fields.Char(string="Reason")
    # stage = fields.Many2many('hr.recruitment.stage',string="Appears on Stage",required=True)


class ApplicantNotMatching(models.TransientModel):
    _name = 'applicant.not.matching.reason'
    _description = 'Not Matching Criteria'

    not_matching_criteria_reason_id = fields.Many2one('hr.applicant.not.matching.reason', 'Not Matching Criteria')
    applicant_ids = fields.Many2many('hr.applicant')

    def action_not_matching_apply(self):
        return self.applicant_ids.write({'not_matching_criteria_reason_id': self.not_matching_criteria_reason_id.id, 'active': False})


class NotMatchingName(models.Model):
    _name = 'hr.applicant.not.matching.reason'

    name = fields.Char(string="Criteria")
    # stage = fields.Many2many('hr.recruitment.stage',string="Appears on Stage",required=True)



class ApplicantNoShow(models.TransientModel):
    _name = 'applicant.no.show.reason'
    _description = 'Get No Show Reason'

    no_show_reason_id = fields.Many2one('hr.applicant.no.show.reason', 'No Show Reason')
    applicant_ids = fields.Many2many('hr.applicant')

    def action_no_show_apply(self):
        return self.applicant_ids.write({'no_show_reason_id': self.no_show_reason_id.id, 'active': False})

class NoShowName(models.Model):
    _name = 'hr.applicant.no.show.reason'

    name = fields.Char(string="Reason")
    # stage = fields.Many2many('hr.recruitment.stage',string="Appears on Stage",required=True) 
