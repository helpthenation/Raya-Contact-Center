# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser
import time
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

class HrEvaluationPlan(models.Model):
    _name = "hr_evaluation.plan"
    _description = "Appraisal Plan"

    name = fields.Char(
        string='Appraisal Plan',
        required=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.user.company_id
    )
    phase_ids = fields.One2many(
        'hr_evaluation.plan.phase',
        'plan_id',
        string='Appraisal Phases',
        copy=True
    )
#    month_first = fields.Integer(
#        string='First Appraisal in (months)',
#        help="This number of months will be used to schedule \
#                the first evaluation date of the employee when\
#                selecting an evaluation plan. ",
#        default=6,
#    )
#    month_next = fields.Integer(
#        string='Periodicity of Appraisal (months)', 
#        help="The number of month that depicts the delay between \
#            each evaluation of this plan (after the first one).",
#        default=12,
#    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )


class HrEvaluationPlanPhase(models.Model):
    _name = "hr_evaluation.plan.phase"
    _description = "Appraisal Plan Phase"
    _order = "sequence"

    name = fields.Char(
        string='Phase',
        # size=64,
        required=True
    )
    sequence = fields.Integer(
        string='Sequence',
        default=1,
    )
    company_id = fields.Many2one(
        'res.company',
        related='plan_id.company_id',
        string='Company',
        store=True,
        readonly=True,
    )
    plan_id = fields.Many2one(
        'hr_evaluation.plan', 
        string='Appraisal Plan',
    )
    action = fields.Selection(
        [('top-down', 'Top-Down Appraisal Requests'),
        ('bottom-up', 'Bottom-Up Appraisal Requests'),
        ('self', 'Self Appraisal Requests'),
        ('final', 'Final Interview')], 
        string='Action',
        required=True,
    )
    survey_id = fields.Many2one(
        'survey.survey',
        string='Appraisal Form',
        required=True
    )
#    send_answer_manager = fields.Boolean(
#        string='All Answers',
#        help="Send all answers to the manager",
#    )
#    send_answer_employee = fields.Boolean(
#        string='All Answers',
#        help="Send all answers to the employee",
#    )
#    send_anonymous_manager = fields.Boolean(
#        string='Anonymous Summary',
#        help="Send an anonymous summary to the manager",
#    )
#    send_anonymous_employee = fields.Boolean(
#        string='Anonymous Summary',
#        help="Send an anonymous summary to the employee",
#    )
    wait = fields.Boolean(
        string='Wait Previous Phases',
        help="Check this box if you want to wait that all preceding phases are finished before launching this phase.",
    )
    # mail_feature = fields.Boolean(
    #     string='Send mail for this phase',
    #     help="Check this box if you want to send mail to employees coming under this phase",
    # )
    # mail_body = fields.Text(
    #     string='Email',
    #     default=lambda *a: _('''
    #     Date: %(date)s
    #     Dear %(employee_name)s,
    #     I am doing an evaluation regarding %(eval_name)s.
    #     Kindly submit your response.
    #     Thanks,
    #     --
    #     %(user_signature)s
    #             '''),
    # )
    # email_subject = fields.Text(
    #     string='Subject',
    #     default=_('''Regarding '''),
    # )


class HrEmployee(models.Model):
#    _name = "hr.employee"
    _inherit="hr.employee"

#    @api.multi
    @api.depends()
    def _appraisal_count(self):
        Evaluation = self.env['hr.evaluation.interview']
        for employee in self:
            user_count = Evaluation.search_count([('user_to_review_id', '=', employee.id)])
            employee.appraisal_count = user_count

    evaluation_plan_id = fields.Many2one(
        'hr_evaluation.plan',
        string='Appraisal Plan',
    )
    evaluation_date = fields.Date(
        string='Next Appraisal Date',
        help="The date of the next appraisal is computed by the appraisal plan's dates (first appraisal + periodicity)."
    )
    appraisal_count = fields.Integer(
        compute='_appraisal_count',
        string='Appraisal Interviews',
    )

#        REMOVE ODOO13
#    def run_employee_evaluation(self, automatic=False, use_new_cursor=False):  # cronjob 
#        now = parser.parse(datetime.now().strftime('%Y-%m-%d'))
#        obj_evaluation = self.env['hr_evaluation.evaluation']
#        emp_ids = self.search([('evaluation_plan_id', '<>', False), ('evaluation_date', '=', False)])
#        for emp in emp_ids:
#            first_date = (now + relativedelta(months=emp.evaluation_plan_id.month_first)).strftime('%Y-%m-%d')
#            emp.write({'evaluation_date': first_date})

#        emp_ids = self.search([('evaluation_plan_id', '<>', False),
#                               ('evaluation_date', '<=', time.strftime("%Y-%m-%d"))])
#        for emp in emp_ids:
#            next_date = (now + relativedelta(months=emp.evaluation_plan_id.month_next)).strftime('%Y-%m-%d')
#            emp.evaluation_date = next_date
#            plan_id = obj_evaluation.create({'employee_id': emp.id,
#                                             'plan_id': emp.evaluation_plan_id.id})
#            plan_id.button_plan_in_progress()
#        return True


class hr_evaluation(models.Model):
    _name = "hr_evaluation.evaluation"
    _inherit = "mail.thread"
    _description = "Employee Appraisal"
    _rec_name = "employee_id"

    date = fields.Date(
        string="Appraisal Deadline",
        default=lambda *a: (parser.parse(datetime.now().strftime('%Y-%m-%d')) + relativedelta(months=+1)).strftime('%Y-%m-%d'),
        required=True,
#         select=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        required=True,
    )
    note_summary = fields.Text(
        string='Appraisal Summary',
    )
    note_action = fields.Text(
        string='Action Plan',
        help="If the evaluation does not meet the expectations, you can propose an action plan",
    )
    rating = fields.Selection(
        [('0', 'Significantly below expectations'),
        ('1', 'Do not meet expectations'),
        ('2', 'Meet expectations'),
        ('3', 'Exceeds expectations'),
        ('4', 'Significantly exceeds expectations')],
        string="Appreciation",
        help="This is the appreciation on which the evaluation is summarized."
    )
    survey_request_ids = fields.One2many(
        'hr.evaluation.interview',
        'evaluation_id',
        string='Appraisal Forms'
    )
    plan_id = fields.Many2one(
        'hr_evaluation.plan', 
        string='Plan',
        required=True,
    )
    state = fields.Selection(
        [('draft', 'New'),
        ('cancel', 'Cancelled'),
        ('wait', 'Plan In Progress'),
        ('progress', 'Waiting Appreciation'),
        ('done', 'Done')],
        string='Status',
        required=False,
        readonly=True,
        copy=False,
        default='draft',
    )
    date_close = fields.Date(
        string='Ending Date',
#         select=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self:self.env.user.company_id.id,
    )
    evaluation_officer_id = fields.Many2one(
        'res.users',
        string='Evaluation Officer',
    )

    #@api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.plan_id.name
            employee = record.employee_id.name
            res.append((record['id'], name + ' / ' + employee))
        return res
    
    #@api.multi
    def onchange_employee_id(self, employee_id):
        vals = {}
        vals['plan_id'] = False
        if employee_id:
            employee_obj = self.env['hr.employee']
            for employee in employee_obj.browse(employee_id):
                if employee and employee.evaluation_plan_id and employee.evaluation_plan_id.id:
                    vals.update({'plan_id': employee.evaluation_plan_id.id})
        return {'value': vals}
    
    #@api.multi
    def button_plan_in_progress(self):
        hr_eval_inter_obj = self.env['hr.evaluation.interview']
        for evaluation in self:
            wait = False
            interview_seq = 1
            for phase in evaluation.plan_id.phase_ids:
                children = []
                if phase.action == "bottom-up":
                    children = evaluation.employee_id.child_ids
                elif phase.action in ("top-down", "final"):
                    if evaluation.employee_id.parent_id:
                        children = evaluation.employee_id.parent_id
#                         children = [evaluation.employee_id.parent_id]
                            # children = evaluation.employee_id.parent_id
                elif phase.action == "self":
#                     children = [evaluation.employee_id]
                    children = evaluation.employee_id

                for child in children:
                    int_id = hr_eval_inter_obj.create({
                        'evaluation_id': evaluation.id,
                        'phase_id': phase.id,
                        'deadline': (parser.parse(datetime.now().strftime('%Y-%m-%d')) + relativedelta(months=+1)).strftime('%Y-%m-%d'),
                        'user_id': child.user_id.id,
                        'interview_seq': interview_seq,
                        # 'user_to_review_id': child.id,
                    })
                    interview_seq += 1
                        
                if phase.wait:
                    wait = True
                if not wait:
                    int_id.survey_req_waiting_answer()
                # if (not wait) and phase.mail_feature:
                #     body = phase.mail_body % {'employee_name': child.name, 'user_signature': child.user_id.signature,
                #         'eval_name': phase.survey_id.title, 'date': time.strftime('%Y-%m-%d'), 'time': time}
                #     sub = phase.email_subject
                #     if child.work_email:
                #         vals = {'state': 'outgoing',
                #                 'subject': sub,
                #                 'body_html': '<pre>%s</pre>' % body,
                #                 'email_to': child.work_email,
                #                 'email_from': evaluation.employee_id.work_email}
                #         self.env['mail.mail'].create(vals)
        self.write({'state': 'wait'})
        return True
    
    #@api.multi
    def button_final_validation(self):
        request_obj = self.env['hr.evaluation.interview']
        self.write({'state': 'progress'})
        for evaluation in self:
            if evaluation.employee_id and evaluation.employee_id.parent_id and evaluation.employee_id.parent_id.user_id.partner_id:
                  # evaluation.message_subscribe_users(user_ids=[evaluation.employee_id.parent_id.user_id.id])
                   evaluation.message_subscribe(partner_ids=[evaluation.employee_id.parent_id.user_id.partner_id.id])
            # print "request_obj.search([('evaluation_id', '=', evaluation.id), ('state', 'in', ['done', 'cancel'])]).ids---",request_obj.search([('evaluation_id', '=', evaluation.id), ('state', 'in', ['done', 'cancel'])]).ids
            if len(evaluation.survey_request_ids.ids) != len(request_obj.search([('evaluation_id', '=', evaluation.id), ('state', 'in', ['done', 'cancel'])]).ids):
                raise Warning(_('You cannot change state, because some appraisal forms have not been completed.'))
        return True
    
    #@api.one
    # def button_done(self):
    #     self.write({'state': 'done', 'date_close': time.strftime('%Y-%m-%d')})
    #     return True
    
    #@api.one
    def button_cancel(self):
        interview_obj = self.env['hr.evaluation.interview']
        self.survey_request_ids.survey_req_cancel()
#         interview_obj.survey_req_cancel([r.id for r in self.survey_request_ids])
        self.write({'state': 'cancel'})
        return True
    
    #@api.one
    def button_draft(self):
        self.write({'state': 'draft'})
        return True
    
    #@api.multi
    # def write(self, vals):
    #     if vals.get('employee_id'):
    #         employee_id = self.env['hr.employee'].browse(vals['employee_id'])
    #         if employee_id.parent_id and employee_id.parent_id.user_id:
    #             vals['message_follower_ids'] = [(4, employee_id.parent_id.user_id.partner_id.id)]
    #     if 'date' in vals:
    #         new_vals = {'deadline': vals.get('date')}
    #         obj_hr_eval_iterview = self.env['hr.evaluation.interview']
    #         for evaluation in self:
    #             for survey_req in evaluation.survey_request_ids:
    #                 survey_req.write(new_vals)
    #     return super(hr_evaluation, self).write(vals)

class HrEvaluationInterview(models.Model):
    _name = 'hr.evaluation.interview'
    _inherit = 'mail.thread'
    _rec_name = 'user_to_review_id'
    _description = 'Appraisal Interview'

    request_id = fields.Many2one(
        'survey.user_input',
        string='Survey Request', 
        readonly=True,
    )
    evaluation_id = fields.Many2one(
        'hr_evaluation.evaluation',
        string='Appraisal Plan',
        required=True
    )
    phase_id =fields.Many2one(
        'hr_evaluation.plan.phase', 
        string='Appraisal Phase',
        required=True
    )
    user_to_review_id = fields.Many2one(
        'hr.employee',
        related='evaluation_id.employee_id',
        string="Employee to evaluate",
    )
    user_id = fields.Many2one(
        'res.users',
        string='Interviewer'
    )
    state = fields.Selection([
        ('draft', "Draft"),
        ('waiting_answer', "In progress"),
        ('done', "Done"),
        ('cancel', "Cancelled")],
        string="State",
        required=True,
        copy=False,
        default='draft',
    )
    survey_id = fields.Many2one(
        'survey.survey',
        related='phase_id.survey_id',
        string="Appraisal Form",
    )
    deadline = fields.Datetime(
        related='request_id.deadline',
        string="Deadline",
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self:self.env.user.company_id.id,
    )
    interview_seq = fields.Integer(
        string='Sequence',
    )
    
    @api.model
    def create(self, vals):
        phase_obj = self.env['hr_evaluation.plan.phase'].browse(vals.get('phase_id'))
        survey_id = phase_obj.read(fields=['survey_id'])[0]['survey_id'][0]
        if vals.get('user_id'):
            user_obj = self.env['res.users'].browse(vals.get('user_id'))
            partner_id = user_obj.partner_id
#            partner_id = user_obj.read(fields=['partner_id'])[0]['partner_id'][0]
        else:
            partner_id = None
        user_input_obj = self.env['survey.user_input']
        if not vals.get('deadline'):
            vals['deadline'] = (datetime.now() + timedelta(days=28)).strftime(DF)
#        ret = user_input_obj.create({'survey_id': survey_id,
#                                              'deadline': vals.get('deadline'),
#                                              'input_type': 'link',
##                                              'type': 'link',
#                                              'partner_id': partner_id})
        ret = phase_obj.survey_id._create_answer(partner=partner_id or False, **{'survey_id': survey_id,
                                                  'deadline': vals.get('deadline'),
                                                  'input_type': 'link',
                                                })#ODOO13
        if ret:
            ret = ret[0]
        vals['request_id'] = ret.id
        return super(HrEvaluationInterview, self).create(vals)
    
    #@api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.survey_id.title
            res.append((record['id'], name))
        return res
    
    #@api.multi
    def survey_req_waiting_answer(self):
#         request_obj = self.env['survey.user_input']
        for interview in self:
            intrview_request_id = interview.evaluation_id.survey_request_ids.filtered(lambda intr_req_id:intr_req_id.phase_id.wait and intr_req_id.state != 'done' and intr_req_id.interview_seq == interview.interview_seq - 1)#ODOO13
            if intrview_request_id:#ODOO13
                raise Warning(_("Not allow to send request untill %s is not Done"%(intrview_request_id.name_get()[0][1])))#ODOO13
            if interview.request_id:
#                interview.request_id.action_survey_resend()
                interview.request_id.action_resend()
            interview.write({'state': 'waiting_answer'})
            intr_mail_template_id = self.env.ref("odoo_hr_evaluation.hr_evaluation_interview_mail_tmpl")
            intr_mail_template_id.send_mail(interview.id)
#            interview.write({'state': 'waiting_answer'})
        return True
    
    #@api.multi
    def survey_req_done(self):
        self.write({'state': 'done'})#ODOO13
        for id in self:
#            flag = False
#            wating_id = 0
            if not id.evaluation_id.id:
                raise Warning(_("You cannot start evaluation without Appraisal."))
            intrview_request_id = id.evaluation_id.survey_request_ids.filtered(lambda intr_req_id:intr_req_id.state == 'draft' and intr_req_id.interview_seq == id.interview_seq + 1) #ODOO13
            if intrview_request_id: #ODOO13
                intrview_request_id[0].survey_req_waiting_answer() #ODOO13
#            records = id.evaluation_id.survey_request_ids
#            for child in records:
#                if child.state == "draft":
##                    wating_id = child.id
#                    wating_id = child #ODOO13
#                    flag = False
#                    continue
#                if child.state != "done":
#                    flag = True
#            if not flag and wating_id:
#                wating_id.survey_req_waiting_answer()
#        self.write({'state': 'done'})#ODOO13
        return True

    #@api.one
    def survey_req_cancel(self):
        self.write({'state': 'cancel'})
        return True
    
    #@api.multi
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        context = self._context.copy()
        response = self.request_id
        context.update({'survey_token': response.token})
        return self.survey_id.with_context(context).action_print_survey()

    #@api.multi
    def action_start_survey(self):
        context = self._context.copy()
        response = self.request_id
        context.update({'survey_token': response.token})
        return self.survey_id.with_context(context).action_start_survey()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
