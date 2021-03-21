# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools,_
from datetime import datetime
from odoo.tools import pycompat, sql
import uuid
from psycopg2 import ProgrammingError
import base64
import logging
import re
from io import BytesIO
from odoo.exceptions import UserError
logger = logging.getLogger(__name__)


class rdt_report(models.Model):
    _name = 'x_wc_recruitment_daily_report_sql'
    _description = 'x_wc_recruitment_daily_report_sql'
    # _inherit = ["sql.request.mixin"]
    _auto = False
    # Prepare Function
    _TTYPE_SELECTION = [
        ("boolean", "boolean"),
        ("char", "char"),
        ("date", "date"),
        ("datetime", "datetime"),
        ("float", "float"),
        ("integer", "integer"),
        ("many2one", "many2one"),
        ("selection", "selection"),
    ]
    # Mapping to guess Odoo field type, from SQL column type
    _SQL_MAPPING = {
        "boolean": "boolean",
        "bigint": "integer",
        "integer": "integer",
        "double precision": "float",
        "numeric": "float",
        "text": "char",
        "character varying": "char",
        "date": "date",
        "timestamp without time zone": "datetime",
    }
    # Created Model Global Private Variable
    # _MODEL_ID = 0
    # Created Fields Global Private Dict
    _FIELDS = []
    # id=fields.Integer()
    # x_create_date=fields.Char(string="Timestamp")
    # x_job_code = fields.Char("Job Code")
    # x_applicant_name = fields.Char("Full Name")
    # x_phone = fields.Char("Mobile number")
    # x_national_id = fields.Char("National ID")
    # x_nationality = fields.Char("Nationality")
    # x_gender = fields.Char("Gender")
    # x_age = fields.Integer("Age")
    # x_governorate = fields.Char("Your Governorate")
    # x_city_area = fields.Char("Where do you live / Area")
    # x_military_status = fields.Char("Military Status")
    # x_graduation_status = fields.Char("Graduation status")
    # x_university = fields.Char("University")
    # x_faculty = fields.Char("Faculty of")
    # x_social_insurance = fields.Char("Do You have Social insurance?")
    # x_email = fields.Char("E-mail Address")
    # x_pc_laptop = fields.Char("Do You Have PC or Laptop?")
    # x_internet_con = fields.Char("Do You have Internet Connection?")
    # x_con_speed = fields.Date("What is your Connection Speed?")
    # x_internet_provider = fields.Char("Connection Provider Name?")
    # x_indebendancy = fields.Char("Do You Prefer Working Independently or within a Team?")
    # x_prev_work_experience = fields.Char("Do you have Previous Work Experience?")
    # x_prev_work_experience_what = fields.Char("What is your Previous work Experience?")
    # x_why_leave = fields.Char("Why do you want to leave your work?")
    # x_why_join = fields.Char("Why do you want this Job?")
    # x_salary_expections = fields.Char("Salary Expections")
    # x_relational_shifts = fields.Char("Are you fine with rotational shifts?")
    # x_english_level = fields.Char("English Level")
    # x_worked_4_raya = fields.Char("Did You work before at Raya?")
    # x_ready_work_from_home = fields.Char("Are You ready to work from home?")
    # x_operating_sys = fields.Char("Your Operating System")
    # x_main_source = fields.Char("Main Source")
    # x_source = fields.Char("Sourcer")
    # x_recruiter = fields.Char("Rec Name")
    # x_hr_interviwe_date = fields.Date("1st Interview Date")
    #
    #
    # x_sales_experience = fields.Char("Sales Experience")
    # x_years_of_experience = fields.Char("Years of Experience")
    #
    #
    # x_first_interview_feedback = fields.Char("HR Interview")
    # x_interview_feedback_reason = fields.Char("Reason Of Rejection")
    # x_sector = fields.Char("Sector")
    # x_project = fields.Char("Project")
    # x_second_interview_feedback = fields.Char("Technical Interview")
    # x_second_interview_feedback_reason = fields.Char("Reason Of Rejection")
    # x_english_test_result = fields.Char("English Test Result")
    #
    # x_pronunciation = fields.Char("Pronunciation")
    # x_grammer = fields.Char("Grammer")
    # x_fluency = fields.Char("Fluency")
    # x_understanding_vocab = fields.Char("Understanding & Vocab")
    #
    # x_typing_test_result = fields.Char("Typing Test Result")
    # x_job_offer_feedback = fields.Char("Signed Offer")
    # x_date_of_signing = fields.Date("Date of Signing")
    # x_job_offer_feedback_reason = fields.Char("Reason of not signing")
    # x_hired = fields.Char("Hired")
    # x_date_of_hiring = fields.Date("Date of Hirirng")
    # x_reason_if_not_hired = fields.Char("Reason of not hired")
    # x_sector_projects_type = fields.Char("Etisalat/Non-Etisalat")

    def init(self):
        print('init')
        print('init')
        print('init')
        # """ RDT main report """
        # # tools.drop_view_if_exists(self._cr, 'x_wc_recruitment_daily_report_sql')
        # self.env.cr.execute('DROP VIEW IF EXISTS x_wc_recruitment_daily_report_sql')
        # self.env.cr.execute(""" CREATE VIEW x_wc_recruitment_daily_report_sql AS (
        #    select
		# applicant.create_date as x_create_date,
	  	# applicant.job_code as x_job_code,
	  	# applicant.partner_name as x_applicant_name,
		# applicant.partner_phone as x_phone,
		# applicant.national_id as x_national_id,
		# country.name as x_nationality,
		# applicant.gender as x_gender,
		# applicant.age as x_age,
		# state_id.name as x_governorate,
		# area_id.name as x_city_area,
		# applicant.military_status as x_military_status,
		# applicant.graduation_status as x_graduation_status,
		# university_id.name as x_university,
		# faculty_id.name as x_faculty,
		# applicant.social_insurance as x_social_insurance,
		# applicant.email_from as x_email,
		# applicant.pc_laptop as x_pc_laptop,
		# applicant.internet_con as x_internet_con,
		# applicant.con_speed as x_con_speed,
		# applicant.internet_provider as x_internet_provider,
		# applicant.indebendancy as x_indebendancy,
		# applicant.prev_work_experience as x_prev_work_experience,
		# applicant.prev_work_experience_what as x_prev_work_experience_what,
		# applicant.why_leave as x_why_leave,
		# applicant.why_join as x_why_join,
        #
		# applicant.salary_expections as x_salary_expections,
        #
		# applicant.rotational_shifts as x_relational_shifts,
		# applicant.english_status as x_english_level,
		# applicant.worked_4_raya as x_worked_4_raya,
		# applicant.ready_work_from_home as x_ready_work_from_home,
		# applicant.operating_sys as x_operating_sys,
		# (Select name from main_utm_source where id = source_id.main_source) as x_main_source,
		# source_id.name as x_source,
        # (Select name from res_partner where id = (Select partner_id from res_users where id = applicant.user_id)) as x_recruiter,
		# applicant.hr_interviwe_date as x_hr_interviwe_date,
		# applicant.sales_experience as x_sales_experience,
		# applicant.years_of_experience as x_years_of_experience,
		# applicant.first_interview_feedback as x_first_interview_feedback,
		# interview_feedback_reason_id.name as x_interview_feedback_reason,
		# (Select name from sector_sector where id = request.sector) as x_sector,
        #
		# project_id.name as x_project,
		# applicant.second_interview_feedback as x_second_interview_feedback,
		# sec_interview_feedback_reason_id.name as x_second_interview_feedback_reason,
		# applicant.english_test_result as x_english_test_result,
        #
        # applicant.pronunciation as x_pronunciation,
		# applicant.grammer as x_grammer,
		# applicant.fluency as x_fluency,
		# applicant.understanding_vocab as x_understanding_vocab,
        #
		# applicant.typing_test_result as x_typing_test_result,
		# CASE WHEN applicant.job_offer_feedback = 'accepted' THEN 'Yes'
        #  ELSE 'No' END AS x_job_offer_feedback,
		# applicant.date_of_signing as x_date_of_signing,
		# job_offer_feedback_reason.name as x_job_offer_feedback_reason,
		# applicant.hired as x_hired,
		# applicant.date_of_hiring as x_date_of_hiring,
		# reason_if_not_hired.name as x_reason_if_not_hired,
		# applicant.sector_projects_type as x_sector_projects_type
        #
        #
		# from hr_applicant applicant
		# inner join res_country country on applicant.nationality = country.id
		# inner join res_country_state state_id on applicant.state = state_id.id
		# inner join city_area area_id on applicant.area = area_id.id
		# inner join hr_institute university_id on applicant.university = university_id.id
		# inner join university_fac faculty_id on applicant.faculty = faculty_id.id
		# inner join utm_source source_id on applicant.source_id = source_id.id
		# inner join res_users recruit_id on applicant.user_id = recruit_id.id
		# inner join interview_feedback interview_feedback_reason_id on applicant.first_interview_feedback_reason = interview_feedback_reason_id.id
		# inner join  hiring_request request on applicant.hiring_request = request.id
		# inner join rcc_project project_id on applicant.project = project_id.id
		# inner join interview_feedback sec_interview_feedback_reason_id on applicant.second_interview_feedback_reason = sec_interview_feedback_reason_id.id
		# inner join interview_feedback job_offer_feedback_reason on applicant.job_offer_feedback_reason = job_offer_feedback_reason.id
		# inner join interview_feedback reason_if_not_hired on applicant.reason_if_not_hired = reason_if_not_hired.id
        #
        # )""")
        self.create_sql_view_and_model_btn()
        # self.button_create_ui()
        # self._prepare_request_for_execution()

    # def _check_execution(self,check = True):
    #     """Ensure that the query is valid, trying to execute it.
    #     a non materialized view is created for this check.
    #     A rollback is done at the end.
    #     After the execution, and before the rollback, an analysis of
    #     the database structure is done, to know fields type."""
    #     # self.ensure_one()
    #
    #     columns = super(rdt_report, self)._check_execution()
    #     print("COLUMNSCOLUMNSCOLUMNSCOLUMNSCOLUMNSCOLUMNS")
    #     print(columns)
    #     print("COLUMNSCOLUMNSCOLUMNSCOLUMNSCOLUMNSCOLUMNS")
    #     field_ids = []
    #     for column in columns:
    #         existing_field = self.bi_sql_view_field_ids.filtered(
    #             lambda x: x.name == column[1]
    #         )
    #         if existing_field:
    #             # Update existing field
    #             field_ids.append(existing_field.id)
    #             existing_field.write({"sequence": column[0], "sql_type": column[2]})
    #         else:
    #             # Create a new one if name is prefixed by x_
    #             if column[1][:2] == "x_":
    #                 field_ids.append(
    #                     sql_view_field_obj.create(
    #                         {
    #                             "sequence": column[0],
    #                             "name": column[1],
    #                             "sql_type": column[2],
    #                             "bi_sql_view_id": self.id,
    #                         }
    #                     ).id
    #                 )
    #
    #     return columns
    # @api.model
    # def _create_savepoint(self):
    #     rollback_name = "{}_{}".format(self._name.replace(".", "_"), uuid.uuid1().hex)
    #     # pylint: disable=sql-injection
    #     req = "SAVEPOINT %s" % (rollback_name)
    #     self.env.cr.execute(req)
    #     return rollback_name
    # @api.model
    # def _rollback_savepoint(self, rollback_name):
    #     # pylint: disable=sql-injection
    #     req = "ROLLBACK TO SAVEPOINT %s" % (rollback_name)
    #     self.env.cr.execute(req)
    # def _hook_executed_request(self):
    #     """Overload me to insert custom code, when the SQL request has
    #     been executed, before the rollback.
    #     """
    #     # self.ensure_one()
    #     return False
    # Action Section
    def create_sql_view_and_model_btn(self):
        print('button_create_sql_view_and_model')
        print('button_create_sql_view_and_model')
        print('button_create_sql_view_and_model')
        # for sql_view in self:
        # Create ORM and access
        self._create_model_and_fields_btn()
        print("KHKDJSKAJDJKASDHKADSJKHKAASDHADSHKADSKHADSJASD")
        print("KHKDJSKAJDJKASDHKADSJKHKAASDHADSHKADSKHADSJASD")
        print("KHKDJSKAJDJKASDHKADSJKHKAASDHADSHKADSKHADSJASD")
        print("KHKDJSKAJDJKASDHKADSJKHKAASDHADSHKADSKHADSJASD")
        self._create_model_access_btn()
        # Create SQL View and indexes
        self._create_view_btn()

    def _create_model_and_fields_btn(self):
        print('_create_model_and_fields')
        print('_create_model_and_fields')
        print('_create_model_and_fields')
        # for sql_view in self:
        # Create model
        model_vals = self._prepare_model_btn()
        print("model_vals")
        print(model_vals)
        print("model_vals")
        model_id = self.env["ir.model"].create(model_vals).id
        # _MODEL_ID = model_id
        print("model_id")
        print(model_id)
        print("model_id")
        rule_id = self.env["ir.rule"].create(self._prepare_rule_btn(model_id)).id
        # Drop table, created by the ORM
        # if sql.table_exists(self._cr, "x_wc_recruitment_daily_report_sql"):
        #     print("ifififdrop")
        #     print("ifififdrop")
        #     print("ifififdrop")
        #     print("ifififdrop")
        #     print("ifififdrop")
        #     req = "DROP TABLE %s" % "x_wc_recruitment_daily_report_sql"
        #     self._log_execute(req)

    def _prepare_request_check_execution_btn(self):
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        """Overload me to replace some part of the query, if it contains
        parameters"""
        query = (""" select
         		applicant.create_date as x_create_date,
         	  	applicant.job_code as x_job_code,
         	  	applicant.partner_name as x_applicant_name,
         		applicant.partner_phone as x_phone,
         		applicant.national_id as x_national_id,
         		country.name as x_nationality,
         		applicant.gender as x_gender,
         		applicant.age as x_age,
         		state_id.name as x_governorate,
         		area_id.name as x_city_area,
         		applicant.military_status as x_military_status,
         		applicant.graduation_status as x_graduation_status,
         		university_id.name as x_university,
         		faculty_id.name as x_faculty,
         		applicant.social_insurance as x_social_insurance,
         		applicant.email_from as x_email,
         		applicant.pc_laptop as x_pc_laptop,
         		applicant.internet_con as x_internet_con,
         		applicant.con_speed as x_con_speed,
         		applicant.internet_provider as x_internet_provider,
         		applicant.indebendancy as x_indebendancy,
         		applicant.prev_work_experience as x_prev_work_experience,
         		applicant.prev_work_experience_what as x_prev_work_experience_what,
         		applicant.why_leave as x_why_leave,
         		applicant.why_join as x_why_join,

         		applicant.salary_expections as x_salary_expections,

         		applicant.rotational_shifts as x_relational_shifts,
         		applicant.english_status as x_english_level,
         		applicant.worked_4_raya as x_worked_4_raya,
         		applicant.ready_work_from_home as x_ready_work_from_home,
         		applicant.operating_sys as x_operating_sys,
         		(Select name from main_utm_source where id = source_id.main_source) as x_main_source,
         		source_id.name as x_source,
                 (Select name from res_partner where id = (Select partner_id from res_users where id = applicant.user_id)) as x_recruiter,
         		applicant.hr_interviwe_date as x_hr_interviwe_date,
         		applicant.sales_experience as x_sales_experience,
         		applicant.years_of_experience as x_years_of_experience,
         		applicant.first_interview_feedback as x_first_interview_feedback,
         		interview_feedback_reason_id.name as x_interview_feedback_reason,
         		(Select name from sector_sector where id = request.sector) as x_sector,

         		project_id.name as x_project,
         		applicant.second_interview_feedback as x_second_interview_feedback,
         		sec_interview_feedback_reason_id.name as x_second_interview_feedback_reason,
         		applicant.english_test_result as x_english_test_result,

                 applicant.pronunciation as x_pronunciation,
         		applicant.grammer as x_grammer,
         		applicant.fluency as x_fluency,
         		applicant.understanding_vocab as x_understanding_vocab,

         		applicant.typing_test_result as x_typing_test_result,
         		CASE WHEN applicant.job_offer_feedback = 'accepted' THEN 'Yes'
                  ELSE 'No' END AS x_job_offer_feedback,
         		applicant.date_of_signing as x_date_of_signing,
         		job_offer_feedback_reason.name as x_job_offer_feedback_reason,
         		applicant.hired as x_hired,
         		applicant.date_of_hiring as x_date_of_hiring,
         		reason_if_not_hired.name as x_reason_if_not_hired,
         		applicant.sector_projects_type as x_sector_projects_type


         		from hr_applicant applicant
         		inner join res_country country on applicant.nationality = country.id
         		inner join res_country_state state_id on applicant.state = state_id.id
         		inner join city_area area_id on applicant.area = area_id.id
         		inner join hr_institute university_id on applicant.university = university_id.id
         		inner join university_fac faculty_id on applicant.faculty = faculty_id.id
         		inner join utm_source source_id on applicant.source_id = source_id.id
         		inner join res_users recruit_id on applicant.user_id = recruit_id.id
         		inner join interview_feedback interview_feedback_reason_id on applicant.first_interview_feedback_reason = interview_feedback_reason_id.id
         		inner join  hiring_request request on applicant.hiring_request = request.id
         		inner join rcc_project project_id on applicant.project = project_id.id
         		inner join interview_feedback sec_interview_feedback_reason_id on applicant.second_interview_feedback_reason = sec_interview_feedback_reason_id.id
         		inner join interview_feedback job_offer_feedback_reason on applicant.job_offer_feedback_reason = job_offer_feedback_reason.id
         		inner join interview_feedback reason_if_not_hired on applicant.reason_if_not_hired = reason_if_not_hired.id
                """)
        return query

    def _prepare_model_btn(self):
        print('_prepare_model')
        print('_prepare_model')
        print('_prepare_model')
        # self.ensure_one()

        # columns = self._check_execution(True)

        # columns = super(rdt_report, self)._check_execution(True)
        # print("columnscolumnscolumnscolumnscolumnscolumnscolumns")
        # print(columns)
        # print("columnscolumnscolumnscolumnscolumnscolumnscolumns")
        field_id = []
        # rollback_name = self._create_savepoint()
        # res = False
        # try:
        #     self.env.cr.execute(query)
        #     res = self._hook_executed_request()
        # except ProgrammingError as e:
        #     logger.exception("Failed query: %s", query)
        #     raise UserError(_("The SQL query is not valid:\n\n %s") % e)
        # finally:
        #     print("***********************************")
        #     print("***********************************")
        #     print("***********************************")
        #     self._rollback_savepoint(rollback_name)
        #     print(res)
        # print("res")
        # print(res)
        # print("res")
        # columns = res
        field_ids = []
        columns = [(1, 'x_create_date', 'timestamp without time zone'), (2, 'x_job_code', 'integer'), (3, 'x_applicant_name', 'character varying'), (4, 'x_phone', 'character varying(32)'), (5, 'x_national_id', 'character varying(14)'), (6, 'x_nationality', 'character varying'), (7, 'x_gender', 'character varying'), (8, 'x_age', 'integer'), (9, 'x_governorate', 'character varying'), (10, 'x_city_area', 'character varying'), (11, 'x_military_status', 'character varying'), (12, 'x_graduation_status', 'character varying'), (13, 'x_university', 'character varying'), (14, 'x_faculty', 'character varying'), (15, 'x_social_insurance', 'character varying'), (16, 'x_email', 'character varying(128)'), (17, 'x_pc_laptop', 'character varying'), (18, 'x_internet_con', 'character varying'), (19, 'x_con_speed', 'character varying'), (20, 'x_internet_provider', 'character varying'), (21, 'x_indebendancy', 'character varying'), (22, 'x_prev_work_experience', 'character varying'), (23, 'x_prev_work_experience_what', 'character varying'), (24, 'x_why_leave', 'character varying'), (25, 'x_why_join', 'character varying'), (26, 'x_salary_expections', 'character varying'), (27, 'x_relational_shifts', 'character varying'), (28, 'x_english_level', 'character varying'), (29, 'x_worked_4_raya', 'character varying'), (30, 'x_ready_work_from_home', 'character varying'), (31, 'x_operating_sys', 'character varying'), (32, 'x_main_source', 'character varying'), (33, 'x_source', 'character varying'), (34, 'x_recruiter', 'character varying'), (35, 'x_hr_interviwe_date', 'date'), (36, 'x_sales_experience', 'character varying'), (37, 'x_years_of_experience', 'integer'), (38, 'x_first_interview_feedback', 'character varying'), (39, 'x_interview_feedback_reason', 'character varying'), (40, 'x_sector', 'character varying'), (41, 'x_project', 'character varying'), (42, 'x_second_interview_feedback', 'character varying'), (43, 'x_second_interview_feedback_reason', 'character varying'), (44, 'x_english_test_result', 'character varying'), (45, 'x_pronunciation', 'integer'), (46, 'x_grammer', 'integer'), (47, 'x_fluency', 'integer'), (48, 'x_understanding_vocab', 'integer'), (49, 'x_typing_test_result', 'character varying'), (50, 'x_job_offer_feedback', 'text'), (51, 'x_date_of_signing', 'timestamp without time zone'), (52, 'x_job_offer_feedback_reason', 'character varying'), (53, 'x_hired', 'character varying'), (54, 'x_date_of_hiring', 'timestamp without time zone'), (55, 'x_reason_if_not_hired', 'character varying'), (56, 'x_sector_projects_type', 'character varying')]
        for column in columns:
            # Create a new one if name is prefixed by x_
            if column[1][:2] == "x_":
                field_ids.append({
                            "sequence": column[0],
                            "name": column[1],
                            "sql_type": column[2],
                        })
                self._FIELDS.append({
                            "sequence": column[0],
                            "name": column[1],
                            "sql_type": column[2],
                        })
        for field in field_ids:
            ttype = False
            for k, v in self._SQL_MAPPING.items():
                if k in field["sql_type"]:
                    ttype = v
            field_id.append((0, 0, {
                "name": field['name'],
                "field_description": field['name'],
                "model_id": False,
                "ttype": ttype,
                "selection": False,
                "relation": False,
            }))
        return {
            "name": 'x_wc_recruitment_daily_report_sql', # Description Of Model
            "model": "x_wc_recruitment_daily_report_sql" , # technical_name
            "access_ids": [],
            "order": 'id asc',
            "field_id": field_id, # Fields
        }
    def _prepare_rule_btn(self, model_id=None):
        print('_prepare_rule')
        print('_prepare_rule')
        print('_prepare_rule')
        # self.ensure_one()
        return {
            "name": _("Access %s") % 'x_wc_recruitment_daily_report_sql',
            "model_id": model_id,
            "global": True,
        }
    # Custom Section
    def _log_execute_btn(self, req):
        print('_log_execute')
        print('_log_execute')
        print('_log_execute')
        _logger.info("Executing SQL Request %s ..." % req)
        self.env.cr.execute(req)
    def _create_model_access(self):
        print('_create_model_access')
        print('_create_model_access')
        print('_create_model_access')
        # for sql_view in self:
        for item in self._prepare_model_access_btn(self.env['ir.model'].search([('model','=','x_wc_recruitment_daily_report_sql')]).id):
            self.env["ir.model.access"].create(item)
    def _prepare_model_access_btn(self,model_id=None):
        print('_prepare_model_access')
        print('_prepare_model_access')
        print('_prepare_model_access')
        # self.ensure_one()
        res = []
        group_id = self.env.ref('base.group_user').id
        group_name = self.env.ref('base.group_user').full_name
        res.append(
            {
                "name": _("%s Access %s") % ("x_wc_recruitment_daily_report_sql", group_name),
                "model_id": model_id,
                "group_id": group_id,
                "perm_read": True,
                "perm_create": True,
                "perm_write": False,
                "perm_unlink": False,
            }
        )
        return res

    def _create_view_btn(self):
        print('_create_view')
        print('_create_view')
        print('_create_view')
        # for sql_view in self:
        self._drop_view_btn()
        try:
            print("11111111222222222233333333344444444555555566666677788889")
            print("11111111222222222233333333344444444555555566666677788889")
            print("11111111222222222233333333344444444555555566666677788889")
            print("11111111222222222233333333344444444555555566666677788889")
            self._log_execute_btn(self._prepare_request_for_execution_btn())
            print("1::L")
            print("1::L")
            print("1::L")
            print("1::L")
            # self._refresh_size()
        except ProgrammingError as e:
            raise UserError(
                _("SQL Error while creating %s VIEW %s :\n %s")
                % ("", "x_wc_recruitment_daily_report_sql", str(e))
            )
    def _drop_view_btn(self):
        print('_drop_view')
        print('_drop_view')
        print('_drop_view')
        # for sql_view in self:
        self._log_execute(
            "DROP %s VIEW IF EXISTS %s"
            % ("", "x_wc_recruitment_daily_report_sql")
        )
        # sql_view.size = False
    def _prepare_request_for_execution_btn(self):
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        print("_prepare_request_for_execution")
        # self.ensure_one()
        xquery = (""" select
         		applicant.create_date as x_create_date,
         	  	applicant.job_code as x_job_code,
         	  	applicant.partner_name as x_applicant_name,
         		applicant.partner_phone as x_phone,
         		applicant.national_id as x_national_id,
         		country.name as x_nationality,
         		applicant.gender as x_gender,
         		applicant.age as x_age,
         		state_id.name as x_governorate,
         		area_id.name as x_city_area,
         		applicant.military_status as x_military_status,
         		applicant.graduation_status as x_graduation_status,
         		university_id.name as x_university,
         		faculty_id.name as x_faculty,
         		applicant.social_insurance as x_social_insurance,
         		applicant.email_from as x_email,
         		applicant.pc_laptop as x_pc_laptop,
         		applicant.internet_con as x_internet_con,
         		applicant.con_speed as x_con_speed,
         		applicant.internet_provider as x_internet_provider,
         		applicant.indebendancy as x_indebendancy,
         		applicant.prev_work_experience as x_prev_work_experience,
         		applicant.prev_work_experience_what as x_prev_work_experience_what,
         		applicant.why_leave as x_why_leave,
         		applicant.why_join as x_why_join,

         		applicant.salary_expections as x_salary_expections,

         		applicant.rotational_shifts as x_relational_shifts,
         		applicant.english_status as x_english_level,
         		applicant.worked_4_raya as x_worked_4_raya,
         		applicant.ready_work_from_home as x_ready_work_from_home,
         		applicant.operating_sys as x_operating_sys,
         		(Select name from main_utm_source where id = source_id.main_source) as x_main_source,
         		source_id.name as x_source,
                 (Select name from res_partner where id = (Select partner_id from res_users where id = applicant.user_id)) as x_recruiter,
         		applicant.hr_interviwe_date as x_hr_interviwe_date,
         		applicant.sales_experience as x_sales_experience,
         		applicant.years_of_experience as x_years_of_experience,
         		applicant.first_interview_feedback as x_first_interview_feedback,
         		interview_feedback_reason_id.name as x_interview_feedback_reason,
         		(Select name from sector_sector where id = request.sector) as x_sector,

         		project_id.name as x_project,
         		applicant.second_interview_feedback as x_second_interview_feedback,
         		sec_interview_feedback_reason_id.name as x_second_interview_feedback_reason,
         		applicant.english_test_result as x_english_test_result,

                 applicant.pronunciation as x_pronunciation,
         		applicant.grammer as x_grammer,
         		applicant.fluency as x_fluency,
         		applicant.understanding_vocab as x_understanding_vocab,

         		applicant.typing_test_result as x_typing_test_result,
         		CASE WHEN applicant.job_offer_feedback = 'accepted' THEN 'Yes'
                  ELSE 'No' END AS x_job_offer_feedback,
         		applicant.date_of_signing as x_date_of_signing,
         		job_offer_feedback_reason.name as x_job_offer_feedback_reason,
         		applicant.hired as x_hired,
         		applicant.date_of_hiring as x_date_of_hiring,
         		reason_if_not_hired.name as x_reason_if_not_hired,
         		applicant.sector_projects_type as x_sector_projects_type


         		from hr_applicant applicant
         		inner join res_country country on applicant.nationality = country.id
         		inner join res_country_state state_id on applicant.state = state_id.id
         		inner join city_area area_id on applicant.area = area_id.id
         		inner join hr_institute university_id on applicant.university = university_id.id
         		inner join university_fac faculty_id on applicant.faculty = faculty_id.id
         		inner join utm_source source_id on applicant.source_id = source_id.id
         		inner join res_users recruit_id on applicant.user_id = recruit_id.id
         		inner join interview_feedback interview_feedback_reason_id on applicant.first_interview_feedback_reason = interview_feedback_reason_id.id
         		inner join  hiring_request request on applicant.hiring_request = request.id
         		inner join rcc_project project_id on applicant.project = project_id.id
         		inner join interview_feedback sec_interview_feedback_reason_id on applicant.second_interview_feedback_reason = sec_interview_feedback_reason_id.id
         		inner join interview_feedback job_offer_feedback_reason on applicant.job_offer_feedback_reason = job_offer_feedback_reason.id
         		inner join interview_feedback reason_if_not_hired on applicant.reason_if_not_hired = reason_if_not_hired.id
                """)
        query = (
            """
            SELECT
                CAST(row_number() OVER () as integer) AS id,
                CAST(Null as timestamp without time zone) as create_date,
                CAST(Null as integer) as create_uid,
                CAST(Null as timestamp without time zone) as write_date,
                CAST(Null as integer) as write_uid,
                my_query.*
            FROM
                (%s) as my_query
        """
            %  xquery
        )
        return "CREATE {} VIEW {} AS ({});".format(
            "", "x_wc_recruitment_daily_report_sql", query,
        )
    def _refresh_size_btn(self):
        print("_refresh_size")
        print("_refresh_size")
        print("_refresh_size")
        print("_refresh_size")
        print("_refresh_size")
        # for sql_view in self:
        req = "SELECT pg_size_pretty(pg_total_relation_size('%s'));" % (
            "x_wc_recruitment_daily_report_sql"
        )
        # self._log_execute(req)
        # self.size = self.env.cr.fetchone()[0]

    # def _create_index(self):
    #     for sql_view in self:
    #         for sql_field in sql_view.bi_sql_view_field_ids.filtered(
    #             lambda x: x.is_index is True
    #         ):
    #             self._log_execute(
    #                 "CREATE INDEX %s ON %s (%s);"
    #                 % (sql_field.index_name, "x_wc_recruitment_daily_report_sql", sql_field.name)
    #             )

    def _prepare_tree_field_btn(self, field={}):
        print("_prepare_tree_field")
        print("_prepare_tree_field")
        print("_prepare_tree_field")
        print("_prepare_tree_field")
        print("_prepare_tree_field")
        # self.ensure_one()
        res = ""
        if field['name']:
            res = """<field name="{}"/>""".format(
                field['name']
            )
        return res

    def _prepare_tree_view_btn(self):
        print("_prepare_tree_view")
        print("_prepare_tree_view")
        print("_prepare_tree_view")
        print("_prepare_tree_view")
        print("_prepare_tree_view")
        print("_prepare_tree_view")
        print("_prepare_tree_view")
        print("_prepare_tree_view")

        # self.ensure_one()
        return {
            "name": 'x_wc_recruitment_daily_report_sql_tree',
            "type": "tree",
            "model": 'x_wc_recruitment_daily_report_sql',
            "arch": """<?xml version="1.0"?>"""
            """<tree string="Analysis">{}"""
            """</tree>""".format(
                "".join([self._prepare_tree_field_btn(x) for x in self._FIELDS])
            ),
        }
    # def _prepare_pivot_field(self):
    #     self.ensure_one()
    #     res = ""
    #     if self.graph_type and self.field_description:
    #         res = """<field name="{}" type="{}" />""".format(self.name, self.graph_type)
    #     return res
    #
    # def _prepare_pivot_view(self):
    #     self.ensure_one()
    #     return {
    #         "name": self.name,
    #         "type": "pivot",
    #         "model": self.model_id.model,
    #         "arch": """<?xml version="1.0"?>"""
    #         """<pivot string="Analysis" stacked="True">{}"""
    #         """</pivot>""".format(
    #             "".join([x._prepare_pivot_field() for x in self.bi_sql_view_field_ids])
    #         ),
    #     }
    def _prepare_action_btn(self, tree_view_id=None):
        print("_prepare_action")
        print("_prepare_action")
        print("_prepare_action")
        print("_prepare_action")
        print("_prepare_action")
        print("_prepare_action")
        print("_prepare_action")
        print("_prepare_action")
        # self.ensure_one()
        # view_mode = self.view_order
        # first_view = view_mode.split(",")[0]
        # if first_view == "tree":
        #     view_id = self.tree_view_id.id
        # elif first_view == "pivot":
        #     view_id = self.pivot_view_id.id
        # else:
        #     view_id = self.graph_view_id.id
        return {
            "name": self._prepare_action_name_btn(),
            "res_model": 'x_wc_recruitment_daily_report_sql',
            "type": "ir.actions.act_window",
            "view_mode": 'tree',
            "view_id": tree_view_id,
            # "search_view_id": self.search_view_id.id,
            # "context": self.action_context,
        }
    def _prepare_action_name_btn(self):
        print("_prepare_action_name")
        print("_prepare_action_name")
        print("_prepare_action_name")
        print("_prepare_action_name")
        print("_prepare_action_name")
        print("_prepare_action_name")
        print("_prepare_action_name")
        print("_prepare_action_name")
        # self.ensure_one()
        # if not self.is_materialized:
        #     return self.name
        return "{} ({})".format(
            'x_wc_recruitment_daily_report_sq++++++s', datetime.utcnow().strftime(_("%m/%d/%Y %H:%M:%S UTC")),
        )

    def _prepare_menu_btn(self, action_id=None):
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        print("_prepare_menu")
        # self.ensure_one()
        print(action_id)
        print(action_id)
        print(action_id)
        return {
            "name": 'x_wc_recruitment_daily_report_sql_menu',
            # "parent_id": self.env.ref("wc_recruitment_daily.menu_report_rdt_raw").id,
            "action": action_id,
            # "sequence": self.sequence,
        }

    def button_create_ui_btn(self):
        print("button_create_ui")
        print("button_create_ui")
        print("button_create_ui")
        print("button_create_ui")
        print("button_create_ui")
        print("button_create_ui")
        print("button_create_ui")
        print("button_create_ui")
        tree_view_id = self.env["ir.ui.view"].create(self._prepare_tree_view_btn()).id

        # self.pivot_view_id = (
        #     self.env["ir.ui.view"].create(self._prepare_pivot_view()).id
        # )
        action_id = self.env["ir.actions.act_window"].create(self._prepare_action_btn(tree_view_id)).id

        menu_vals = self._prepare_menu_btn(action_id)
        print("menu_vals")
        print(menu_vals)
        print("menu_vals")
        menu_id = self.env["ir.ui.menu"].create(menu_vals).id
