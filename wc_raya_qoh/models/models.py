# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


        
class qoh_report(models.Model):
    _name = 'wc_raya_qoh.report'
    _description = 'wc_raya_qoh.report'
    _auto = False

    id=fields.Integer()
    x_tower=fields.Char(string="Tower")
    x_working_location = fields.Char("Working Location")
    x_sector = fields.Char("Sector")
    x_partner_id = fields.Char("Contact")
    x_project = fields.Char("Project")
    x_level_name = fields.Char("English level")
    x_request_id = fields.Char("Request")
    x_batch = fields.Integer("Batch")
    x_training_start_date = fields.Date("Training Start Date")
    x_source_id = fields.Char("Source")
    x_medium_id = fields.Char("Medium")
    x_name = fields.Char("Name")
    x_phone = fields.Char("Phone")
    x_national_id = fields.Char("National ID")
    x_age = fields.Char("Age")
    x_faculty = fields.Char("Faculty")
    x_area_id = fields.Char("Area")
    x_graduated = fields.Char("Graduation Status")
    x_hc_date = fields.Date("HC date")
    x_days = fields.Float("Days")
    x_qoh = fields.Char("QOH")
    x_reason_id = fields.Char("Reason")

    def init(self):
        """ QOH main report """
        # tools.drop_view_if_exists(self._cr, 'wc_raya_qoh_report')
        self.env.cr.execute('DROP VIEW IF EXISTS wc_raya_qoh_report')
        self.env.cr.execute(""" CREATE VIEW wc_raya_qoh_report AS (
           SELECT row_number() OVER () as id,
tower.name as x_tower,
work.name as x_working_location,
sector.name as x_sector,
partner_id.name as x_partner_id,
project.name as x_project,
level.name as x_level_name,
request.name as x_request_id,
request.batch_numbers as x_batch,
applicant.training_start_date as x_training_start_date,
source_id.name as x_source_id,
medium_id.name as x_medium_id,
applicant.name as x_name,
applicant.partner_phone as x_phone,
applicant.national_id as x_national_id,
applicant.age as x_age,
fac_id.name as x_faculty,
area_id.name as x_area_id,
CASE WHEN applicant.graduation_status = 'graduated' THEN 'Yes'
           WHEN applicant.graduation_status = 'notgraduated' THEN 'No' 
           Else ''
END as x_graduated,
CASE WHEN (applicant.training_start_date > applicant.drop_date) AND (applicant.training_start_date > applicant.quality_of_hiring_date)  THEN applicant.training_start_date 
           WHEN (applicant.drop_date> applicant.training_start_date ) AND (applicant.drop_date> applicant.quality_of_hiring_date)  THEN applicant.drop_date
           WHEN (applicant.quality_of_hiring_date> applicant.training_start_date ) AND (applicant.quality_of_hiring_date> applicant.drop_date)  THEN applicant.quality_of_hiring_date
           
END as x_hc_date,
TRUNC(DATE_PART('day', applicant.training_start_date::timestamp - (CASE WHEN (applicant.training_start_date > applicant.drop_date) AND (applicant.training_start_date > applicant.quality_of_hiring_date)  THEN applicant.training_start_date::timestamp
           WHEN (applicant.drop_date> applicant.training_start_date ) AND (applicant.drop_date> applicant.quality_of_hiring_date)  THEN applicant.drop_date::timestamp
           WHEN (applicant.quality_of_hiring_date> applicant.training_start_date ) AND (applicant.quality_of_hiring_date> applicant.drop_date)  THEN applicant.quality_of_hiring_date::timestamp END )::timestamp)/7) as x_days,

CASE WHEN (applicant.tarinee_status = 'dropped') THEN 'NO'
           WHEN (applicant.tarinee_status = 'active') AND (applicant.quality_of_hiring_date::timestamp  > NOW()::timestamp ) THEN 'YES'     
           Else ''
END as x_qoh,
applicant.tarinee_status,
reason_id.name as x_reason_id

FROM hr_applicant applicant 
inner join hiring_request request on request.id = applicant.hiring_request
inner join wc_raya_qoh_tower tower on tower.id = request.tower
inner join work_locations work on work.id = request.working_location
inner join sector_sector sector on sector.id = request.sector
inner join res_users user_id on user_id.id = applicant.user_id
inner join res_partner partner_id on partner_id.id = user_id.partner_id 
inner join rcc_project project on project.id = request.project
inner join utm_source source_id on source_id.id = applicant.source_id
inner join utm_medium medium_id on medium_id.id = applicant.medium_id
inner join university_fac fac_id on fac_id.id=applicant.faculty 
inner join city_area area_id on area_id.id=applicant.area
inner join drop_reasons reason_id on reason_id.id=applicant.drop_reason
inner join emp_lang_skills skill on  skill.applicant_id = applicant.id
inner join lang_levels level on  level.id = skill.applicant_level and applicant.job_category = 'operational'
        )""")

class drp_report(models.Model):
    _name = 'wc_raya_qoh.reason'
    _description = 'wc_raya_qoh.reason'
    _auto = False

    id = fields.Integer()
    x_dropout_reason=fields.Char("Drop out reason")

    def init(self):
        """ QOH main report """
        self.env.cr.execute('DROP VIEW IF EXISTS wc_raya_qoh_reason')
        self.env.cr.execute(""" 
        CREATE VIEW wc_raya_qoh_reason AS (
        SELECT row_number() OVER () as id,

         CASE WHEN applicant.drop_reason IS Not NULL THEN 'Reached'
            Else 'unreachable'
         END as x_dropout_reason
 
         From hr_applicant applicant 

where applicant.job_category='operational'

        );
        """)
        




