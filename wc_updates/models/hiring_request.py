# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    
    english_test_result = fields.Char('English Test Result')
    typing_test_result = fields.Char('Typing Test Result')
    hr_interviwe_date = fields.Date(string="HR Interview Date")
    technical_interviwe_date = fields.Date(string="Technical Interview Date")
    full_name_arabic = fields.Char('Arabic full name')
    date_of_birth = fields.Date('Date of Birth  ')
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
    area = fields.Many2one('city.area',string="Area")
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

# class HRJOB(models.Model):
#     _inherit = 'hr.job'
#     prooject = fields.Many2one('rcc.project',string="Project")    