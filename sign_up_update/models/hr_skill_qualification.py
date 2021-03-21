# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
from datetime import datetime
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = 'res.partner'
    techskill_ids = fields.One2many(
        'hr.skill.clone', 'partner_tech_talent_id', 'Technical Skills')
    nontechskill_ids = fields.One2many(
        'hr.skill.clone', 'partner_non_tech_talent_id', 'Non-Technical Skills')
    education_ids = fields.One2many(
        'profile.education', 'partner_id', 'Education')
    certification_ids = fields.One2many(
        'profile.certification', 'partner_id', 'Certification')
    profession_ids = fields.One2many(
        'profile.profession.job', 'partner_id', 'Professional Experience')

class EmployeeEducation(models.Model):
    _name = 'profile.education'
    _description = 'Employee Education'

    partner_id = fields.Many2one('res.partner', 'Profile')
    type_id = fields.Many2one('hr.recruitment.degree',
                              "Degree", ondelete="cascade")
    institute_id = fields.Many2one(
        'hr.institute', 'Institutes', ondelete="cascade")
    score = fields.Char()
    qualified_year = fields.Date()
    doc = fields.Binary('Transcripts')

class EmployeeCertification(models.Model):
    _name = 'profile.certification'
    _description = 'Portal Certification'
    
    partner_id = fields.Many2one('res.partner', 'Profile')
    course_id = fields.Many2one('cert.cert', 'Course Name', ondelete="cascade")
    levels = fields.Char('Bands/Levels of Completion')
    year = fields.Date('Year of completion')
    doc = fields.Binary('Certificates')



class EmployeeProfessionJob(models.Model):
    _name = 'profile.profession.job'
    _description = 'Profile Profession'
    partner_id = fields.Many2one('res.partner', 'Profile')
    job_id = fields.Many2one('res.partner', 'Profile')
    location = fields.Char()
    period=fields.Char()
    doc = fields.Binary('Experience Certificates')