# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)x
from werkzeug import urls
# from odoo import _,api,fields,models
from odoo import _,api,fields,models, tools, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

# class RCCPROJECT(models.Model):
#     _inherit = 'rcc.project'
#
#     departments = fields.Many2many('hr.department', compute="_compute_departments")
#     def _compute_departments(self):
#         for this in self:
#             pass
class Departments(models.Model):
    _inherit = 'hr.department'

    raya_department = fields.Boolean()
    projects = fields.Many2many('rcc.project')
    @api.constrains('raya_department')
    def _constrains_raya_department(self):
        for rec in self:
            if not rec.raya_department:
                if len(rec.projects) <= 0:
                    raise UserError(_('You should add at least one project if the department is not related to company'))
    @api.onchange('raya_department')
    def clear_old(self):
        if len(self.projects) > 0 and self.raya_department:
            self.projects = False


class HiringReq(models.Model):
    _inherit = "hiring.request"


    users_who_approved = fields.Many2many('hr.employee','already_approved_rel')

    @api.onchange('state')
    def checkapproved(self):
        if self.department_gm_approval_required == True and self.state != 'draft':
            if self.department_approved == False and self.state != 'draft':
                raise UserError('Please ask director to approve first')
        if self.approvers_approved == False and self.state != 'draft':
            raise UserError('Please ask approvers to approve first')

    def apprpve_request(self):
        if self.env.user.id == self.center.manager_id.user_id.id:
            self.department_approved = True
            if self.center.manager_id.job_id in self.hiring_request_approvers.mapped('job_id'):
                self.users_who_approved = [(6,0,[self.env.user.employee_id.id])]
            else:
                pass
            self.write({'state':'director_approved'})
    def user_approve(self):
        old_approved_emps = self.users_who_approved.ids
        old_approved_positions = self.users_who_approved.mapped('job_id')
        if self.env.user.employee_id.job_id in old_approved_positions:
            raise UserError(_('An employee with your job position already approved'))
        else:
            if self.env.user.employee_id.id in self.hiring_request_approvers.ids:
                old_approved_emps.append(self.env.user.employee_id.id)
            else:
                raise UserError(_('You can not approve this hiring request'))
        self.users_who_approved = [(6,0,old_approved_emps)]
        if len(self.users_who_approved.mapped('job_id')) == len(self.hiring_request_approvers.mapped('job_id')):
            self.approvers_approved = True
            self.state = 'approved'




    is_dept_director = fields.Boolean(compute="_compute_is_dept_director")
    def _compute_is_dept_director(self):
        for this in self:
            current_user_emp_id = this.env.user.employee_id.id
            this.is_dept_director = False
            if this.dept_director.id == current_user_emp_id:
                this.is_dept_director = True
    can_approve = fields.Boolean(compute="_compute_can_approve")
    def _compute_can_approve(self):
        for this in self:
            current_user_emp_id = this.env.user.employee_id.id
            this.can_approve = False
            if len(this.hiring_request_approvers.filtered(lambda x:x.id == current_user_emp_id)) > 0:
                this.can_approve = True
            if this.is_dept_director:
                this.can_approve = True
    already_approved = fields.Boolean(compute="_compute_already_approved")
    def _compute_already_approved(self):
        for this in self:
            current_user_emp_id = this.env.user.employee_id.id
            this.already_approved = False
            if len(this.users_who_approved.filtered(lambda x:x.id == current_user_emp_id)) > 0:
                this.already_approved = True
            if this.dept_director.id == current_user_emp_id and this.department_approved:
                this.already_approved = True

    job_id = fields.Many2one(
        'hr.job', 'HR Job Position')
    actual_hired = fields.Integer('Actual Hiring')
    @api.onchange('category')
    def chng_job_category(self):
        if self.category:
            if self._context.get('default_category',False):
                if self.category != self._context.get('default_category'):
                    self.write({'category':self._context.get('default_category')})
                    raise UserError(_('You are not allowed to use this category !'))

    department_gm_approval_required = fields.Boolean(string="Department Director Approval")
    dept_director = fields.Many2one('hr.employee','Department Director',compute="_compute_dept_director")
    def _compute_dept_director(self):
        for this in self:
            this.dept_director = False
            if this.require_hiring_request_type:
                if this.hiring_request_type:
                    if this.job:
                        if this.job.request_approvals.filtered(lambda x:x.type == this.hiring_request_type):
                            if this.job.request_approvals.filtered(lambda x:x.type == this.hiring_request_type).department_director:
                                this.dept_director = this.center.manager_id
                                this.department_gm_approval_required = True
    department_approved = fields.Boolean(string="Director Approved")
    approvers_approved = fields.Boolean(string="Approvers Approved")
    allowed_hiring_request_type = fields.Many2many('hiring.request.types','hiring_request_many_rel', compute="_compute_allowed_hiring_request_type")
    require_hiring_request_type = fields.Boolean(compute="_compute_allowed_hiring_request_type")

    @api.onchange('job')
    def _compute_allowed_hiring_request_type(self):
        for this in self:
            this.allowed_hiring_request_type = False
            this.require_hiring_request_type = False
            if this.job:
                list_allowed = []
                for line in this.job.request_approvals:
                    list_allowed.append(line.type.id)
                this.allowed_hiring_request_type = [(6,0,list_allowed)]
                if len(this.allowed_hiring_request_type) > 0 :
                    this.require_hiring_request_type = True

    hiring_request_type = fields.Many2one('hiring.request.types',string="Request Types")
    hiring_request_approvers = fields.Many2many('hr.employee','hiring_emp_approvers_rel',string="Request Approvers")
    @api.onchange('job','hiring_request_type','center')
    def _compute_hiring_request_approvers(self):
        for this in self:
            # if this.state != 'draft':
            #     pass
            # else:
            if this.require_hiring_request_type:
                if this.hiring_request_type:
                    list_emps = []
                    line = this.job.request_approvals.filtered(lambda x:x.type == this.hiring_request_type)
                    if line.department_director:
                        if not this.center.manager_id:
                            raise UserError(_('The hiring request type needs a department director to be set at department page '))
                    required = line.position
                    for pos in line.position:
                        emps_for_this_positions = self.env['hr.employee'].search([('job_id','=',pos.id),('raya_team','=',True)])
                        for id in emps_for_this_positions.ids:
                            list_emps.append(id)
                    founded_emps = self.env['hr.employee'].browse(list_emps)
                    founded_emps_jobs = founded_emps.mapped('job_id')
                    if len(required) != len(founded_emps_jobs):
                        raise UserError(_('Company dose not have sufficient employees for required jobs'))
                    if len(list_emps) <= 0:
                        this.hiring_request_approvers = False
                    else:
                        this.hiring_request_approvers = [(6,0,list_emps)]
                else:
                    this.hiring_request_approvers = False
            else:
                this.hiring_request_approvers = False

    state = fields.Selection([
        ("draft", "Draft"),("director_approved", "Director Approved "),("approved", "Confirmed / Approved "),
        ("rejected", "Rejected"),("done", "Finished and Closed")],
            string="Status",
            index=True,
            track_visibility="onchange",
            required=True,
            default="draft"
        )

    @api.onchange('job')
    def chanegeCenter(self):
        self.center = self.job.department_id
#    department required in job position
#    manager required on department



class HiringReqTypes(models.Model):
    _name = 'hiring.request.types'
    #Example -  New ( hiring request types )
    name = fields.Char(string="Name")
    department_director = fields.Boolean(string="Department Director")
    description = fields.Text(string="Description")
    position = fields.Many2many('hr.job',string="Approvers",domain=[('job_category','=','talent')])

class JobApprovals(models.Model):
    _name = 'job.approvals'

    type = fields.Many2one('hiring.request.types')
    @api.onchange('type')
    def fill_table(self):
        if self.type:
            self.department_director = self.type.department_director
            self.position = self.type.position
    department_director = fields.Boolean(string="Department Director")
    position = fields.Many2many('hr.job',string="Approvers",domain=[('job_category','=','talent')])
    job_id = fields.Many2one('hr.job')
class HiringReqTypes(models.Model):
    _inherit = 'hr.job'
    request_approvals= fields.One2many('job.approvals','job_id',string="Request Types")
    #Approvers Positions
    #Description
    #Name
    hiring_request_many = fields.Many2many(
       'hiring.request', 'request_job_id_rel','id','job_id', 'Hiring Request')
    # def read(self, fields=None, load='_classic_read'):
    #     res = super(HiringReqTypes, self).read(fields, load)
    #     for this in self:
    #         if this.job_category == 'talent':
    #             no_of_recruitment = 0.0
    #             for hr in this.hiring_request_many.filtered(lambda x:x.state == 'approved'):
    #                 print(hr)
    #                 print(hr.total_heads)
    #                 no_of_recruitment += hr.total_heads
    #             print(no_of_recruitment)
    #             this.no_of_recruitment = no_of_recruitment
    #     return res
    @api.onchange('job_category')
    def chng_job_category(self):
        if self.job_category:
            if self._context.get('default_job_category',False):
                if self.job_category != self._context.get('default_job_category'):
                    self.write({'job_category':self._context.get('default_job_category')})
                    raise UserError(_('You are not allowed to use this category please, please reselect the correct category !'))




class hrrecruitmentsourceEXT(models.Model):
    _inherit = "hr.recruitment.source"
    project = fields.Many2one('rcc.project',required=True)
    hiring_request = fields.Many2one('hiring.request',string="Hiring Request")
    recruiter = fields.Many2one('res.users',string="Recruiter",)

    @api.depends('job_id')
    def _get_current_user(self):
        for r in self:
            r.recruiter = self.env.user

    @api.onchange('hiring_request','recruiter')
    def _change_project(self):
        for r in self:
            r.recruiter = self.env.user
        self.project = self.hiring_request.project

    @api.onchange('project','hiring_request','recruiter')
    def _change_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for source in self:
            source.url = urls.url_join(base_url, "%s?%s" % (source.job_id.website_url,
                urls.url_encode({
                    'utm_campaign': self.env.ref('hr_recruitment.utm_campaign_job').name,
                    'utm_medium': self.env.ref('utm.utm_medium_website').name,
                    'utm_project':self.project.id,
                    'utm_hiring_request':self.hiring_request.id,
                    'recruiter':self.recruiter.id,
                    'utm_source': source.source_id.name
                })
            ))

class hrJobEXT(models.Model):
    _inherit = "hr.job"
    hiring_request_many = fields.Many2many(
        'hiring.request', 'request_job_id_rel','id','job_id', 'Hiring Request')
    def read(self, fields=None, load='_classic_read'):
        res = super(hrJobEXT, self).read(fields, load)
        for this in self:
            if this.job_category == 'talent':
                no_of_recruitment = 0.0
                for hr in this.hiring_request_many.filtered(lambda x:x.state == 'approved'):
                    no_of_recruitment += hr.total_heads
                this.no_of_recruitment = no_of_recruitment
                print(no_of_recruitment)
        return res
    @api.onchange('job_category')
    def chng_job_category(self):
        if self.job_category:
            if self._context.get('default_job_category',False):
                if self.job_category != self._context.get('default_job_category'):
                    self.write({'job_category':self._context.get('default_job_category')})
                    raise UserError(_('You are not allowed to use this category please, please reselect the correct category !'))

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    job_category = fields.Selection([('talent','Talent Aqcusiotion'),('operational','Operational')],string="Job Category")
    stage_id = fields.Many2one('hr.recruitment.stage', 'Stage', ondelete='restrict', tracking=True,
                               compute='_compute_stage', store=True, readonly=False,
                               domain="['|', ('job_category', '=', False), ('job_category', '=', job_category)]",
                               copy=False, index=True,
                               group_expand='_read_group_stage_ids')
    @api.depends('job_id')
    def _compute_stage(self):
        for applicant in self:
            if applicant.job_id:
                if not applicant.stage_id:
                    stage_ids = self.env['hr.recruitment.stage'].search([
                        '|',
                        ('job_category', '=', False),
                        ('job_category', '=', applicant.job_category),
                        ('fold', '=', False)
                    ], order='sequence asc', limit=1).ids
                    applicant.stage_id = stage_ids[0] if stage_ids else False
            else:
                applicant.stage_id = False

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # retrieve job_id from the context and write the domain: ids + contextual columns (job or default)
        job_category = self._context.get('default_job_category')
        search_domain = [('job_category', '=', False)]
        if job_category:
            search_domain = ['|', ('job_category', '=', job_category)] + search_domain
        # if stages:
        #     search_domain = ['|', ('id', 'in', stages.ids)] + search_domain
        # for line in stages:
        #     print(line.job_category)
        # print(search_domain)
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        # for st in stages.browse(stage_ids):
        #     print(st.job_category)
        return stages.browse(stage_ids)
