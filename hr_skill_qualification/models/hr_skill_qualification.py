# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
from datetime import datetime
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.job'
    job_category = fields.Selection([('talent','Talent Aqcusiotion'),('operational','Operational')],string="Job Category")


    def _tech_val(self):
        val = self.env['hr.skill.type'].search([('skill_type','=','technical')])
        self.tech = val
    def _nontech_val(self):
        val = self.env['hr.skill.type'].search([('skill_type','=','non_technical')])
        self.nontech = val
    def _lang_val(self):
        val = self.env['hr.skill.type'].search([('skill_type','=','language')])
        self.lang = val

    tech = fields.Many2one('hr.skill.type', default=lambda self: self.env['hr.skill.type'].search([('skill_type','=','technical')]), compute= _tech_val)
    nontech = fields.Many2one('hr.skill.type', default=lambda self: self.env['hr.skill.type'].search([('skill_type','=','non_technical')]), compute= _nontech_val)
    lang = fields.Many2one('hr.skill.type', default=lambda self: self.env['hr.skill.type'].search([('skill_type','=','language')]), compute= _lang_val)

    prooject = fields.Many2one('rcc.project',string="Project")
    techskill_ids = fields.One2many(
        'emp.tech.skills', 'employee_id', 'Technical Skills')
    nontechskill_ids = fields.One2many(
        'emp.nontech.skills', 'employee_id', 'Non-Technical Skills')
    education_ids = fields.One2many(
        'employee.education', 'employee_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'employee_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession.job', 'job_id', 'Professional Experience')
    language_level_ids =  fields.One2many('emp.lang.skills', 'employee_id', 'Language Level')

    ######################################################################
    # Talent skills for job position

    # techskill_talent_ids =  fields.Many2many('hr.employee.skill', 'job_tech_skil_rel', 'job_id', 'tech_skill_id', 'Technical Skills')

    techskill_talent_ids = fields.One2many(
        'hr.skill.clone.job', 'job_tech_talent_id', 'Technical Skills')
    nontechskill_talent_ids = fields.One2many(
        'hr.skill.clone.job', 'job_non_tech_talent_id', 'Non-Technical Skills')
    language_level_talent_ids =  fields.One2many(
        'hr.skill.clone.job', 'job_lang_talent_id', 'Language Level')

    ######################################################################

class EmployeeTechSkills(models.Model):
    _name = 'emp.tech.skills'
    _description = 'Employee Tech Skills'

    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.job', 'Job')
    tech_id = fields.Many2one(
        'tech.tech', 'Technical Skills', ondelete="cascade")
    levels = fields.Selection([('basic', 'Basic'),
                               ('medium', 'Medium'),
                               ('advance', 'Advance')], 'Levels')
    applicant_level = fields.Selection([('basic', 'Basic'),
                               ('medium', 'Medium'),
                               ('advance', 'Advance')], 'Applicant Level')
    employee_level = fields.Many2one('hr.skill.level', 'Employee Level', readonly=True)
    validation_date = fields.Date('Validation Date', readonly=True)

class MainSource(models.Model):
    _name = 'main.utm.source'

    name = fields.Char()

class MainSource(models.Model):
    _inherit = 'utm.source'

    main_source = fields.Many2one('main.utm.source')

class EmployeeTechSkills(models.Model):
    _name = 'emp.lang.skills'
    _description = 'Employee language levels'
    tech_id = fields.Many2one('lang.tech', 'Language', ondelete="cascade")
    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.job', 'Job')
    levels = fields.Many2one('lang.levels', 'Levels')
    applicant_level = fields.Many2one('lang.levels', 'Applicant Level')

    employee_level = fields.Many2one('hr.skill.level', 'Employee Level', readonly=True)
    validation_date = fields.Date('Validation Date', readonly=True)

class TechTech(models.Model):
    _name = 'lang.tech'
    _description = 'Language'
    name = fields.Char()

class TechTech(models.Model):
    _name = 'tech.tech'
    _description = 'Tech Tech'

    name = fields.Char()

    def unlink(self):
        """
        his method is called user tries to delete a skill which
        is already in use by an employee.
        --------------------------------------------------------
        @param self : object pointer
        """
        tech_skill = self.env['emp.tech.skills'].search(
            [('tech_id', 'in', self.ids)])
        if tech_skill:
            raise UserError(
                _('You are trying to delete a Skill which is referenced by an Employee.'))
        return super(TechTech, self).unlink()

class EmployeeNonTechSkills(models.Model):
    _name = 'emp.nontech.skills'
    _description = 'Employee Non Tech Skills'

    applicant_id = fields.Many2one('hr.applicant', 'Applicant')
    employee_id = fields.Many2one('hr.job', 'Job')
    nontech_id = fields.Many2one(
        'nontech.nontech', 'Non-Technical Skills', ondelete="cascade")
    levels = fields.Selection([('basic', '1'),
                               ('medium', '2'),
                               ('advance', '3'),
                               ('4_advance', '4'),
                               ('5_advance', '5')], 'Levels')
    applicant_level = fields.Selection([('basic', '1'),
                               ('medium', '2'),
                               ('advance', '3'),
                               ('4_advance', '4'),
                               ('5_advance', '5')], 'Applicant Level')

    employee_level = fields.Many2one('hr.skill.level', 'Employee Level', readonly=True)
    validation_date = fields.Date('Validation Date', readonly=True)

class NontechNontech(models.Model):
    _name = 'nontech.nontech'
    _description = 'Nontech Nontech'

    name = fields.Char()

    def unlink(self):
        """
        This method is called user tries to delete a skill which
        is already in use by an employee.
        --------------------------------------------------------
        @param self : object pointer
        """
        tech_skill = self.env['emp.nontech.skills'].search(
            [('nontech_id', 'in', self.ids)])
        if tech_skill:
            raise UserError(
                _('You are trying to delete a Skill \
                    which is referenced by an Employee.'))
        return super(NontechNontech, self).unlink()

class EmployeeEducation(models.Model):
    _name = 'employee.education'
    _description = 'Employee Education'


    partner_id = fields.Many2one('res.partner', 'partner')
    emp_id = fields.Many2one('hr.employee', 'employee')
    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.job', 'Job')
    type_id = fields.Many2one('hr.recruitment.degree',
                              "Degree", ondelete="cascade")
    institute_id = fields.Many2one(
        'hr.institute', 'Institutes', ondelete="cascade")
    score = fields.Char()
    qualified_year = fields.Date()
    doc = fields.Binary('Transcripts')

class HrInstitute(models.Model):
    _name = 'hr.institute'
    _description = 'Hr Institute'

    name = fields.Char()
    country_id = fields.Many2one('res.country', 'Country')
    state_id = fields.Many2one('res.country.state', 'State')

class Univeristy_fac(models.Model):
    _name='university.fac'
    name=fields.Char()

class EmployeeCertification(models.Model):
    _name = 'employee.certification'
    _description = 'Employee Certification'

    partner_id = fields.Many2one('res.partner', 'partner')
    emp_id = fields.Many2one('hr.employee', 'employee')
    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.job', 'Job')
    course_id = fields.Many2one('cert.cert', 'Course Name', ondelete="cascade")
    levels = fields.Char('Bands/Levels of Completion')
    year = fields.Date('Year of completion')
    doc = fields.Binary('Certificates')

class CertCert(models.Model):
    _name = 'cert.cert'
    _description = 'Cert Cert'

    name = fields.Char('Course Name')

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    prev_work_experience_what = fields.Char(string="What is your Previous work Experience?",attrs="{'required':[('prev_work_experience','=','Yes')],'invisible':[('prev_work_experience','!=','Yes')]}")

    why_leave = fields.Char(string="Why do you want to leave your work?",attrs="{'required':[('prev_work_experience','=','Yes')],'invisible':[('prev_work_experience','!=','Yes')]}")

    why_join= fields.Char(string="Why do you want this Job?",attrs="{'required':[('prev_work_experience','=','Yes')],'invisible':[('prev_work_experience','!=','Yes')]}")

    salary_expections = fields.Char(string="Do you have Previous Work Experience?",attrs="{'required':[('prev_work_experience','=','Yes')],'invisible':[('prev_work_experience','!=','Yes')]}")
    rotational_shifts= fields.Selection([('Yes','Yes'),
                                        ('No','No')],string="Are you fine with rotational shifts?",attrs="{'required':[('prev_work_experience','=','Yes')],'invisible':[('prev_work_experience','!=','Yes')]}")
    hr_interviwe_date = fields.Date(string="HR Interview Date")
    technical_interviwe_date = fields.Date(string="Technical Interview Date")

class EmployeeProfession(models.Model):
    _name = 'employee.profession'
    _description = 'Employee Profession'

    applicant_id = fields.Many2one('hr.applicant', 'applicant')
    employee_id = fields.Many2one('hr.Job', 'Job')
    job_id = fields.Many2one('hr.job', 'Job Title')
    location = fields.Char()
    from_date = fields.Date('Start Date')
    to_date = fields.Date('End Date')
    doc = fields.Binary('Experience Certificates')

class EmployeeProfessionJob(models.Model):
    _name = 'employee.profession.job'
    _description = 'Employee Profession'

    partner_id = fields.Many2one('res.partner', 'partner')
    emp_id = fields.Many2one('hr.employee', 'employee')
    job_id = fields.Many2one('hr.job', 'Job Title')
    applicant_id = fields.Many2one('hr.applicant', 'Job Title')

    location = fields.Char()
    period=fields.Char()

    from_date = fields.Date('Start Date')
    to_date = fields.Date('End Date')
    doc = fields.Binary('Experience Certificates')

class HrTalent(models.Model):
    _name = 'hr.skill.clone.job'

    skill_type_id = fields.Many2one('hr.skill.type')
    skill_id = fields.Many2one('hr.skill')
    skill_level_id = fields.Many2one('hr.skill.level')

    ##################################################################
    ###### hr.job
    ##################################################################
    job_tech_talent_id = fields.Many2one('hr.job')
    job_non_tech_talent_id = fields.Many2one('hr.job')
    job_lang_talent_id = fields.Many2one('hr.job')
    ###############################################################

    @api.onchange('skill_type_id')
    def _update_skills_domain(self):
        if self.skill_type_id:
            ids = self.env['hr.skill'].search([('skill_type_id', '=', self.skill_type_id.id)]).ids
            return {
                'domain': {
                    'skill_id': [('id', 'in', ids)],
                }
            }
    @api.onchange('skill_id')
    def _update_levels_domain(self):
        print(self.skill_type_id.name)
        print(self.skill_id.name)

        if self.skill_level_id.id == False:
            if self.skill_type_id.id and self.skill_id.id:
                # cur_levels = self.env['hr.skill.level'].search()
                cur_levels = self.skill_type_id.mapped('skill_level_ids').ids
                ids = []

                rel = "("
                for level in cur_levels:
                    if level == cur_levels[-1]:
                        rel += str(level) +")"
                    else:
                        rel += str(level) +","

                sql = "SELECT level_id from hr_level_to_skills_rel where level_id in" +str(rel)+ " and skill_id = "+ str(self.skill_id.id)+" ;"
                self._cr.execute(sql)
                result = self._cr.fetchall()
                for value in result:
                    ids.append(value[0])

                print("in the method to end")
                print("in the method to end")

                return {
                    'domain': {
                        'skill_level_id': [('id', 'in', ids)],
                    }
                }


class HrTalent(models.Model):
    _name = 'hr.skill.clone'

    skill_type_id = fields.Many2one('hr.skill.type')
    skill_id = fields.Many2one('hr.skill')
    skill_level_id = fields.Many2one('hr.skill.level')

    ##################################################################
    ###### res.partner
    ##################################################################
    partner_tech_talent_id = fields.Many2one('res.partner')
    partner_non_tech_talent_id = fields.Many2one('res.partner')
    partner_lang_talent_id = fields.Many2one('res.partner')
    ###############################################################

    nontech_applicant_talent_level = fields.Many2one('hr.skill.level')
    tech_applicant_talent_level = fields.Many2one('hr.skill.level')
    lang_applicant_talent_level = fields.Many2one('hr.skill.level')

    @api.onchange('skill_type_id')
    def _update_skills_domain(self):
        if self.skill_type_id:
            ids = self.env['hr.skill'].search([('skill_type_id', '=', self.skill_type_id.id)]).ids
            return {
                'domain': {
                    'skill_id': [('id', 'in', ids)],
                }
            }

    @api.onchange('skill_id')
    def _update_levels_domain(self):
        print(self.skill_type_id.name)
        print(self.skill_id.name)

        if self.skill_level_id.id == False:
            if self.skill_type_id.id and self.skill_id.id:
                # cur_levels = self.env['hr.skill.level'].search()
                cur_levels = self.skill_type_id.mapped('skill_level_ids').ids
                ids = []

                rel = "("
                for level in cur_levels:
                    if level == cur_levels[-1]:
                        rel += str(level) +")"
                    else:
                        rel += str(level) +","

                sql = "SELECT level_id from hr_level_to_skills_rel where level_id in" +str(rel)+ " and skill_id = "+ str(self.skill_id.id)+" ;"
                self._cr.execute(sql)
                result = self._cr.fetchall()
                for value in result:
                    ids.append(value[0])

                print("in the method to end")
                print("in the method to end")
                print("in the method to end")

                return {
                    'domain': {
                        'skill_level_id': [('id', 'in', ids)],
                    }
                }


class HrTalent(models.Model):
    _name = 'hr.skill.clone.applicant'

    skill_type_id = fields.Many2one('hr.skill.type')
    skill_id = fields.Many2one('hr.skill')
    skill_level_id = fields.Many2one('hr.skill.level')

    ##################################################################
    ###### hr.applicant
    ##################################################################
    applicant_tech_talent_id = fields.Many2one('hr.applicant')
    applicant_non_tech_talent_id = fields.Many2one('hr.applicant')
    applicant_lang_talent_id = fields.Many2one('hr.applicant')

    nontech_applicant_talent_level = fields.Many2one('hr.skill.level')
    nontech_employee_talent_level = fields.Many2one('hr.skill.level', readonly=True)
    nontech_validation_talent_date = fields.Date( readonly=True)
    nontech_level_domain = fields.Many2many('hr.skill.level', 'applicant_nontech_level_domain_rel', 'nontech_applicant_talent_level' , 'level_id')

    tech_applicant_talent_level = fields.Many2one('hr.skill.level')
    tech_employee_talent_level = fields.Many2one('hr.skill.level', readonly=True)
    tech_validation_talent_date = fields.Date(readonly=True)
    tech_level_domain = fields.Many2many('hr.skill.level', 'applicant_tech_level_domain_rel', 'tech_applicant_talent_level' , 'level_id')

    lang_applicant_talent_level = fields.Many2one('hr.skill.level')
    lang_employee_talent_level = fields.Many2one('hr.skill.level', readonly=True)
    lang_validation_talent_date = fields.Date(readonly=True)
    lang_level_domain = fields.Many2many('hr.skill.level', 'applicant_lang_level_domain_rel', 'lang_applicant_talent_level', 'level_id')
    ###############################################################





    @api.onchange('skill_type_id')
    def _update_skills_domain(self):
        if self.skill_type_id:
            ids = self.env['hr.skill'].search([('skill_type_id', '=', self.skill_type_id.id)]).ids
            return {
                'domain': {
                    'skill_id': [('id', 'in', ids)],
                }
            }
    @api.onchange('skill_id')
    def _update_levels_domain(self):
        print(self.skill_type_id.name)
        print(self.skill_id.name)

        if self.skill_level_id.id == False:
            if self.skill_type_id.id and self.skill_id.id:
                # cur_levels = self.env['hr.skill.level'].search()
                cur_levels = self.skill_type_id.mapped('skill_level_ids').ids
                ids = []

                rel = "("
                for level in cur_levels:
                    if level == cur_levels[-1]:
                        rel += str(level) +")"
                    else:
                        rel += str(level) +","

                sql = "SELECT level_id from hr_level_to_skills_rel where level_id in" +str(rel)+ " and skill_id = "+ str(self.skill_id.id)+" ;"
                self._cr.execute(sql)
                result = self._cr.fetchall()
                for value in result:
                    ids.append(value[0])

                print("in the method to end")
                print("in the method to end")

                return {
                    'domain': {
                        'skill_level_id': [('id', 'in', ids)],
                    }
                }

class HrApplicant(models.Model):
    _inherit = 'res.partner'

    techskill_talent_ids = fields.One2many(
        'hr.skill.clone', 'partner_tech_talent_id', 'Technical Skills')
    nontechskill_talent_ids = fields.One2many(
        'hr.skill.clone', 'partner_non_tech_talent_id', 'Non-Technical Skills')
    language_level_talent_ids =  fields.One2many(
        'hr.skill.clone', 'partner_lang_talent_id', 'Language Level')

    education_ids = fields.One2many(
        'employee.education', 'partner_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'partner_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession.job', 'partner_id', 'Professional Experience')


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    job_category = fields.Selection([('talent','Talent Aqcusiotion'),('operational','Operational')],string="Job Category")

    def _tech_val(self):
        val = self.env['hr.skill.type'].search([('skill_type','=','technical')])
        self.tech = val
    def _nontech_val(self):
        val = self.env['hr.skill.type'].search([('skill_type','=','non_technical')])
        self.nontech = val
    def _lang_val(self):
        val = self.env['hr.skill.type'].search([('skill_type','=','language')])
        self.lang = val

    tech = fields.Many2one('hr.skill.type', default=lambda self: self.env['hr.skill.type'].search([('skill_type','=','technical')]), compute= _tech_val)
    nontech = fields.Many2one('hr.skill.type', default=lambda self: self.env['hr.skill.type'].search([('skill_type','=','non_technical')]), compute= _nontech_val)
    lang = fields.Many2one('hr.skill.type', default=lambda self: self.env['hr.skill.type'].search([('skill_type','=','language')]), compute= _lang_val)

    emp_flag = fields.Boolean(default=False)
    @api.onchange('emp_id')
    def update_emp_flag(self):
        if self.emp_id.id:
            self.emp_flag = True
        else:
            self.emp_flag = False

    english_test_result = fields.Char('English Test Result')
    typing_test_result = fields.Char('Typing Test Result')

    techskill_ids = fields.One2many(
        'emp.tech.skills', 'applicant_id', 'Technical Skills')
    nontechskill_ids = fields.One2many(
        'emp.nontech.skills', 'applicant_id', 'Non-Technical Skills')
    education_ids = fields.One2many(
        'employee.education', 'applicant_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'applicant_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession.job', 'applicant_id', 'Professional Experience')
    language_level_ids =  fields.One2many('emp.lang.skills', 'applicant_id', 'Language Level')

    ######################################################################
    # Talent skills for applicant
    techskill_talent_ids = fields.One2many(
        'hr.skill.clone.applicant', 'applicant_tech_talent_id', 'Technical Skills')
    nontechskill_talent_ids = fields.One2many(
        'hr.skill.clone.applicant', 'applicant_non_tech_talent_id', 'Non-Technical Skills')
    language_level_talent_ids =  fields.One2many(
        'hr.skill.clone.applicant', 'applicant_lang_talent_id', 'Language Level')
    ######################################################################


    date_of_birth = fields.Date('Date of Birth  ')
    full_name_arabic = fields.Char('Arabic full name')
    age = fields.Integer('Age')
    gender =fields.Selection([('male','Male'),('female','Female')],string="Gender")
    state = fields.Many2one('res.country.state',string="Governorate")

    nationality = fields.Many2one('res.country',string="Nationality")
    military_status = fields.Selection([('Completed','Completed'),
                                        ('Will serve','Will serve'),
                                        ('Exempted','Exempted'),
                                        ('Postponed','Postponed'),
                                        ('Female','Female')
                                        ],string="Military Status")
    graduation_status = fields.Selection([('graduated','Graduated'),
                                        ('notgraduated','Under Grade')],string="Graduation status" )
    university = fields.Many2one('hr.institute',string="Your University ?")
    faculty = fields.Many2one('university.fac',string="Your Faculty ?")
    english_status = fields.Selection([('Fluent','Fluent'),
                                        ('Excellent','Excellent'),
                                        ('V.Good','V.Good'),
                                        ('Good','Good'),
                                        ('Fair','Fair')],string="Your English Level ? ")
    social_insurance = fields.Selection([('Yes','Yes'),
                                        ('No','No')],string="Do You have Social insurance? ")
    worked_4_raya= fields.Selection([('Yes','Yes'),
                                        ('No','No')], string="Did You work before at Raya? ")

    pc_laptop= fields.Selection([('Yes','Yes'),
                                        ('No','No')], string="Do You Have PC or Laptop?")
    internet_con= fields.Selection([('Yes','Yes'),
                                        ('No','No')], string="Do You have Internet Connection?")

    con_speed = fields.Selection([('less_10','Less than 10 Mbps'),
                                        ('10 Mbps','10 Mbps'),
                                        ('More10Mbps','More than 10 Mbps')], string="What is your Connection Speed?")
    internet_provider = fields.Selection([('WE','WE'),('vodafone','Vodafone'),('Orange','Orange'),('Other','Other')],
        string="Connection Provider Name?")

    type_of_connection = fields.Selection([('adsl','ADSL'),
        ('adsl','ADSL'),
        ('mobile_data','Mobile Data'),
        ('other','Other')],string="Type Of Connection")

    ready_work_from_home = fields.Selection([('Yes','Yes'),
                                        ('No','No')], string="Are You ready to work from home?")

    operating_sys = fields.Selection([('Windows XP','Windows XP'),
                                        ('Windows 7','Windows 7'),
                                        ('Windows 8','Windows 8'),
                                        ('Windows 10','Windows 10'),
                                        ('Linux','Linux'),
                                        ('macOS','macOS'),
                                        ('Unix','Unix')], string="Your Operating System ?")

    indebendancy= fields.Selection([('Independently','Independently'),
                            ('Within a Team','Within a Team'),
                            ('Both','Both')], string="Do You Prefer Working Independently or within a Team?")

    prev_work_experience = fields.Selection([('Yes','Yes'),
                                        ('No','No')], string="Do you have Previous Work Experience?")
    training_start_date= fields.Date('Training Start Date')
    quality_of_hiring_date = fields.Date('Quality Of Hiring')

    first_interview_feedback = fields.Selection([('accepted','Accepted'),('rejected','Rejected'),('refuse','Refuse'),('lost_interest','Lost Interest'),('not_matching_criteria','Not Matching Criteria'),('no_show','No Show')],string='First Interview Feedback')
    second_interview_feedback = fields.Selection([('accepted','Accepted'),('rejected','Rejected'),('refuse','Refuse'),('lost_interest','Lost Interest'),('not_matching_criteria','Not Matching Criteria'),('no_show','No Show')],string='Second Interview Feedback')
    client_review_feedback = fields.Selection([('accepted','Accepted'),('rejected','Rejected'),('refuse','Refuse'),('lost_interest','Lost Interest'),('not_matching_criteria','Not Matching Criteria'),('no_show','No Show')],string='Client Interview Feedback')
    job_offer_feedback = fields.Selection([('accepted','Accepted'),('rejected','Rejected'),('refuse','Refuse'),('lost_interest','Lost Interest'),('not_matching_criteria','Not Matching Criteria'),('no_show','No Show')],string="Job Offer Feedback")

    first_interview_feedback_reason = fields.Many2one('interview.feedback','First Interview Feedback Reason')
    second_interview_feedback_reason = fields.Many2one('interview.feedback','Second Interview Feedback Reason')
    client_review_feedback_reason = fields.Many2one('interview.feedback','Client Interview Feedback Reason')
    job_offer_feedback_reason = fields.Many2one('interview.feedback','Job Offer Feedback Reason')

    ###############new for reports
    #application
    job_code = fields.Integer('Job Code')
    _sql_constraints = [
        ('unique_job_code', 'unique (job_code)', 'Job Code already exists!')
    ]
    years_of_experience = fields.Integer('Years of Experience')
    sales_experience = fields.Selection([('yes','Yes'),('no','No')],string="Sales Experience")
    #feedback
    date_of_signing = fields.Datetime('Date of Signing')
    hired = fields.Selection([('yes','Yes'),('no','No')],string="Hired")
    date_of_hiring = fields.Datetime('Date of Hiring')
    reason_if_not_hired = fields.Many2one('interview.feedback','Reason if not hired')
    sector_projects_type = fields.Selection([('banking','Banking'),('etisalat','Etisalat'),('non_etisalat','Non-Etisalat')],string="Sector Projects Type")
    #Answers
    pronunciation = fields.Integer('Pronunciation')
    grammer = fields.Integer('Grammer')
    fluency = fields.Integer('Fluency')
    understanding_vocab = fields.Integer('Understanding & Vocab')
    #related fields
    # applicant_name = fields.Char(related="partner_id.name")
    # national_id = fields.Char(related="partner_id.national_id")
    # nationality = fields.Char(related="nationality.name")
    # governorate = fields.Char(related="state.name")







    tarinee_status = fields.Selection([('active','Active'),('dropped','Dropped')],string="Trainee Status")
    joined_training = fields.Selection([('yes','Yes'),('no','No')],string="Joined Training")
    not_joining_reason = fields.Char('Reason')
    drop_date =  fields.Date('Drop Date')
    drop_reason =fields.Many2one('drop.reasons',string="Drop Reasons")

    def _default_project(self):
        return self.job_id.prooject.id

    project = fields.Many2one('rcc.project',string="Project",default=lambda self: self._default_project())

    @api.onchange('training_start_date')
    def training_start_datechg(self):
        if self.training_start_date:
            self.quality_of_hiring_date = self.training_start_date + timedelta(days=90)

#    @api.onchange('job_id')
 #   def ProJectCalc(self):
 #       self.project = self.job_id.prooject

class EmployeeTechSkills(models.Model):
    _name = 'drop.reasons'
    _description = "Drop Reasons"

    name = fields.Char('Reason')

class EmployeeinterviewFeedback(models.Model):
    _name = 'interview.feedback'
    _description = 'Interview Feedback'

    name = fields.Char('Feedback')

class EmployeeTechSkills(models.Model):
    _name = 'emp.lang.skills2'

    tech_id = fields.Many2one('lang.tech', 'Language', ondelete="cascade")
    applicant_id = fields.Many2one('hr.applicant', 'applicant')

    levels = fields.Many2one('lang.levels', 'Levels')
    applicant_level = fields.Many2one('lang.levels', 'Applicant Level')

    employee_level = fields.Many2one('hr.skill.level', 'Employee Level', readonly=True)
    validation_date = fields.Date('Validation Date', readonly=True)



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    education_ids = fields.One2many(
        'employee.education', 'emp_id', 'Education')
    certification_ids = fields.One2many(
        'employee.certification', 'emp_id', 'Certification')
    profession_ids = fields.One2many(
        'employee.profession.job', 'emp_id', 'Professional Experience')
