# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError


class raya_refuse(models.TransientModel):
    _inherit = 'applicant.get.refuse.reason'

    reason_type = fields.Selection([('reason','Refuse Reason'),('lost_interest','Lost Interest Reason'),('not_match','Not Matching Criteria'),('no_show','No Show Reason')])
    job_category = fields.Selection([('talent','Talent'),('operational','Operational')])
    linker1=fields.One2many('reason.refuse','quality')
    linker2=fields.One2many('hr.applicant','quality_hold')
    quality=fields.Boolean(compute="check_quality")
    quality_hold=fields.Boolean(compute="check_quality_hold")
    def check_quality_hold(self):
        for this in self:
            this.quality_hold=this.linker2.quality_hold
    def check_quality(self):
        for this in self:
            this.quality=this.linker1.quality
    @api.onchange('reason_type')
    def update_refuse_id_domain(self):
        reason_ids=[]
        if self.reason_type:
            reason_ids = self.env['reason.refuse'].search([('reason_type','=',self.reason_type)]).ids

        self.job_category = self.env['hr.applicant'].browse(self.env.context.get('active_id')).job_category

        flag = self.env.user.has_group('wc_raya_quality.system_hr_recruitment_quality_team')
        if flag:
            return {
                    'domain': {
                        'applicant_reason_id': [('quality', '=',True),('id', 'in', reason_ids)],
                    }
            }
        else:
            return {
                    'domain': {
                        'applicant_reason_id': [('id', 'in', reason_ids),('quality', '=',False)],
                    }
            }


    applicant_reason_id = fields.Many2one('reason.refuse', "Reason")
    note = fields.Text('Note')


    def action_refuse_reason_apply(self): #last override on wc_ta_extention
        if self.applicant_ids:
            if not self.applicant_ids.partner_id:
                if self.applicant_ids.email_from:
                    partner_id = self.env['res.partner'].search([('email','=',self.applicant_ids.email_from)])
                    if len(partner_id) == 1:
                        self.applicant_ids.write({'partner_id':partner_id.id})
                    else:
                        partner_id = self.env['res.partner'].create({
                        'name':self.applicant_ids.name.replace("'s Application",""),
                        'email':self.applicant_ids.email_from,
                        'mobile':self.applicant_ids.partner_mobile,
                        'phone':self.applicant_ids.partner_phone,
                        'national_id':self.applicant_ids.national_id,
                        })
                        self.applicant_ids.write({'partner_id':partner_id.id})
        template_id = self.env['mail.template'].search([('refuse_email_template','=',True)],limit=1)
        template_id.send_mail(self.applicant_ids.id,force_send=True)
        self.applicant_ids.write({'refuse_reason_id': self.refuse_reason_id.id, 'active': False})
        if self.job_category == 'operational':
            self.applicant_ids.write({
                                    'refuse_reason_id': self.refuse_reason_id.id,
                                    'operational_refuse_note': self.note,
                                    'active': False
                                    })
        elif self.job_category == 'talent':
            self.applicant_ids.write({
                                    'talent_refuse_reason_type': self.reason_type,
                                    'talent_refuse_reason_id': self.applicant_reason_id.id,
                                    'talent_refuse_note': self.note,
                                    'active': False,
                                    'quality':False
                                    })
        return True

        # return True
        # ir_model_data = self.env['ir.model.data']
        # try:
        #     template_id = self.env['mail.template'].search([('refuse_email_template','=',True)],limit=1).id
        # except ValueError:
        #     template_id = False
        # try:
        #     compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        # except ValueError:
        #     compose_form_id = False
        #
        # ctx = {
        #     'default_use_template': True,
        #     'default_template_id': template_id,
        #     'default_composition_mode': 'comment',
        #     'force_email': True,
        #     'default_partner_ids':[(6,0,[self.applicant_ids.partner_id.id])]
        # }
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form_id, 'form')],
        #     'view_id': compose_form_id,
        #     'target': 'new',
        #     'context': ctx,
        # }
        # else:
            # return self.applicant_ids.write({'refuse_reason_id': self.refuse_reason_id.id, 'active': False})




class HrApplicantRefuse(models.Model):
    _inherit = 'hr.applicant'

    # operational_refuse_reason_type = fields.Selection([('reason','Refuse Reason'),('lost_interest','Lost Interest Reason'),('not_match','Not Matching Criteria'),('no_show','No Show Reason')], readonly=True)
    operational_refuse_note = fields.Text(readonly=True)
    talent_refuse_reason_type = fields.Selection([('reason','Refuse Reason'),('lost_interest','Lost Interest Reason'),('not_match','Not Matching Criteria'),('no_show','No Show Reason')], readonly=True)
    talent_refuse_reason_id = fields.Many2one('reason.refuse', 'Refuse Reason', readonly=True)
    quality = fields.Boolean('Quality', default=False)
    talent_refuse_note = fields.Text(readonly=True)

class RayaRefuseReason(models.Model):
    """docstring for RayaRefuseReason."""
    _name = 'reason.refuse'

    name = fields.Char("Reason", required=True)
    reason_type = fields.Selection([('reason','Refuse Reason'),('lost_interest','Lost Interest Reason'),('not_match','Not Matching Criteria'),('no_show','No Show Reason')], required=True)
    quality = fields.Boolean('Quality', default=False)
