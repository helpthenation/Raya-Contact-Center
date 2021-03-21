# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrJob(models.Model):
    _inherit = 'hr.job'

    resume_line_ids = fields.One2many('wc_ta_qualification.hr.resume.line', 'job_id', string="JOB Qualifications")

class HiringRequest(models.Model):
    _inherit = "hiring.request"

    resume_line_ids = fields.One2many('wc_ta_qualification.hr.resume.line', 'hr_id', string=" Hiring Request Qualification Lines")

class hrApplicant(models.Model):
    _inherit = "hr.applicant"

    resume_line_ids = fields.One2many('wc_ta_qualification.hr.resume.line', 'applicant_id', string="Qualification Lines")
    employee_job_category=fields.Selection([('talent','Talent'),('operational','Operational')],compute='compute_cate')

    def compute_cate(self):
        for this in self:
            this.employee_job_category=this.emp_id.job_id.job_category

class Employee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        application = self.env['hr.applicant']
        if self.env.context.get('default_applicant_id'):
            application = self.env['hr.applicant'].browse(self.env.context.get('default_applicant_id')[0])
        else:
            pass
        if len(application)==1:
            listt = []
            for line in application.resume_line_ids:
                listt.append((0,0,{
                'name':line.name,
                'date_start':line.date_start,
                'date_end':line.date_end,
                'description':line.description,
                'line_type_id':line.line_type_id.id,
                'display_type':line.display_type,
                }))
            vals['resume_line_ids'] = listt
        res = super(Employee, self).create(vals)
        employee= self.env['hr.resume.line'].search([('employee_id','=',res.id),('name','=',res.company_id.name)])
        employee.update({'name': res.job_title or '',
        'description':  res.company_id.name or '',})
        return res

class wc_ta_qualification(models.Model):
    _name = 'wc_ta_qualification.hr.resume.line'
    _description = 'wc_ta_qualification.hr.resume.line'

    applicant_id = fields.Many2one('hr.applicant', required=False, ondelete='cascade')
    job_id = fields.Many2one('hr.job', required=False, ondelete='cascade')
    hr_id = fields.Many2one('hiring.request', required=False, ondelete='cascade')
    name = fields.Char(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    description = fields.Text(string="Description")
    line_type_id = fields.Many2one('hr.resume.line.type', string="Type")

    display_type = fields.Selection([('classic', 'Classic'),('certification','Certification')], string="Display Type", default='classic')

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end OR date_end = NULL))", "The start date must be anterior to the end date."),
    ]
