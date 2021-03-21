# -*- coding: utf-8 -*-

import json
import random
import uuid
import werkzeug
from random import randint
from odoo import api, fields, exceptions, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError
import re
from odoo.exceptions import AccessError
from odoo.osv import expression
from odoo.tools import is_html_empty
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import requests
import http.client

#Connect Zone Api Parameters 
class HIRINGRequests(models.Model):
    _inherit = 'hiring.request'

    CZID = fields.Integer("Connect Zone ID")
    
    def hrrequest_cz_call(self):
        ##############################################################################
        #####################     GENERAL VARIABLES         ##########################
        ##############################################################################
        # Date
        CURR_DATE = datetime.today().strftime('%Y/%m/%d')
        CURR_DATE = '2021/01/20'
        # Category
        CATEGORY = "1"
        # URL Params Concatunate 
        PARAMS = "?date="+CURR_DATE+"&category="+CATEGORY
        #Base URL
        URL = "recruitment-api.rayacx.com/api/cz/"
        # URL + Concatunate
        URL = URL+"Gethiringrequests"+PARAMS
        # Connection 
        print("Connect ZONE")
        print("Connect ZONE")
        print("Connect ZONE")
        print("Connect ZONE")
        conn = http.client.HTTPSConnection("recruitment-api.rayacx.com")
        payload = ''
        #Headers 
        headers = {'Authorization': 'Bearer UUvQxe3uvXDTMH7lriK6le0IeLkw3hkZC7Kn_eErH6o2SROhFAXj2TKR-bwYZ3O0OCoc7x08LHYdPxyk8VkO_5t3tLHoJoJzEj_AswoDDazBwdqhAZ2q6t2rw1Jvn9ytMC5lCd8KHbfdbvWoj-_X79Fkzm-mL9PRu_LWpC6vjssExpAWtT_EePWcD3zQPYIISelMaGA0XE-z3n291ZMAoA'}
        ##############################################################################
        # Request Access Endpoint Calling
        ##############################################################################
        ##############################################################################
        conn.request("GET", "/api/cz/Gethiringrequests?date="+str(CURR_DATE)+"&category=1", payload, headers)
        res = conn.getresponse()
        # Reading Data
        data = res.read()
        dict_data = json.loads(data.decode('utf-8'))
        print(data.decode('utf-8'))
        for i in dict_data:
            #Get odoo Center ID
            center = self.env['hr.department'].search([('name','=',str(i['workingCenter']))],limit=1).id
            
            #If Dosn,t Exist Create
            if not center:
                center = self.env['hr.department'].create({'name':str(i['workingCenter']),
                                                           'project_ids': [(6, 0,{'name'})]})
                center = center.id
            
            #Get odoo Location  ID
            location = self.env['work.locations'].search([('name','=',str(i['workingLocations']))],limit=1).id
            
            #If Dosn,t Exist Create
            if not location:
                location = self.env['work.locations'].create({'name':str(i['workingLocations'])})
                location = location.id
                
            # Search fro Job
            job = self.env['hr.job'].search([('name','=',str(i['jobTitle']))],limit=1).id
            
            if job:            
                job_category = self.env['hr.job'].search([('name','=',str(i['jobTitle']))],limit=1).job_category
                if job_category:
                    if job_category == "talent":
                        job_category="Talent Acq"
                EXIST_OBJ =  self.env['hiring.request'].search([('CZID','=',str(i['hiringRequestID']))])
                #Exist Object
                if EXIST_OBJ:
                    # Writ Existing Hiring Request
                    EXIST_OBJ.write({
                        "CZID":str(i['hiringRequestID']),
                        "name":str(i['hiringRequestID']),
                        "category":job_category,
                        "center":center,
                        "working_location":location,
                        "job":job,
                        "total_heads":str(i['totalHeads']),
                        "total_males":str(i['totalMales']),
                        "total_females":str(i['totalFemales']),
                        "batch_numbers":str(i['batchNumber'])
                        })
                else:
                    # Create Hiring Request
                    self.create({
                            "CZID":str(i['hiringRequestID']),
                            "name":str(i['hiringRequestID']),
                            "category":job_category,
                            "center":center,
                            "working_location":location,
                            "job":job,
                            "total_heads":str(i['totalHeads']),
                            "total_males":str(i['totalMales']),
                            "total_females":str(i['totalFemales']),
                            "batch_numbers":str(i['batchNumber'])
                            #"center":
                        })

#class EmployeesKPI(models.Model):
#    _inherit = 'employee_kpi_data'
    
#    CZKPI_CZ = fields.Char("Connect Zone KPI ID")
    
class EmployeesHR(models.Model):
    _inherit = 'hr.employee'
    
    CZID = fields.Integer("Connect Zone Employee ID")
    CZHRID = fields.Integer("Connect Zone Employee ID")
    Applicable= fields.Boolean()
    def UpdateApplicantStatus(self):
        conn = http.client.HTTPSConnection("recruitment-api.rayacx.com")
        
        headers = {'Authorization': 'Bearer UUvQxe3uvXDTMH7lriK6le0IeLkw3hkZC7Kn_eErH6o2SROhFAXj2TKR-bwYZ3O0OCoc7x08LHYdPxyk8VkO_5t3tLHoJoJzEj_AswoDDazBwdqhAZ2q6t2rw1Jvn9ytMC5lCd8KHbfdbvWoj-_X79Fkzm-mL9PRu_LWpC6vjssExpAWtT_EePWcD3zQPYIISelMaGA0XE-z3n291ZMAoA'}
        refid = "11"
        is_egyption = "true"
        if self.nationality.id == 65:
            refid = self.national_id
        else:
            refid = self.passport_id
            is_egyption = "false"
        hiring_date = self.training_start_date
            
        payload = "IsEgyption="+is_egyption+"&RefId="+refid+"&Hiringdate="+hiring_date
        conn.request("POST", "/api/cz/UpdateApplicantStatus?IsEgyption=true&RefId=15236555&Hiringdate=2017-08-01", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

class hrApplicant(models.Model):
    _inherit = 'hr.applicant'
    
    passport_id = fields.Char("Passport ID")
    CZID = fields.Integer("Connect Zone Employee ID")
    CZHRID = fields.Integer("Connect Zone Employee ID")
#
#    @api.onchange('training_start_date')
#    def UpdateApplicantStatus(self):
#        conn = http.client.HTTPSConnection("recruitment-api.rayacx.com")
        
#        headers = {'Authorization': 'Bearer UUvQxe3uvXDTMH7lriK6le0IeLkw3hkZC7Kn_eErH6o2SROhFAXj2TKR-bwYZ3O0OCoc7x08LHYdPxyk8VkO_5t3tLHoJoJzEj_AswoDDazBwdqhAZ2q6t2rw1Jvn9ytMC5lCd8KHbfdbvWoj-_X79Fkzm-mL9PRu_LWpC6vjssExpAWtT_EePWcD3zQPYIISelMaGA0XE-z3n291ZMAoA'}
#        refid = "11"
#       is_egyption = "true"
#        if self.nationality.id == 65:
#            refid = self.national_id
#        else:
#            refid = self.passport_id
#            is_egyption = "false"
#        hiring_date = self.training_start_date
#            
#        payload = "IsEgyption="+is_egyption+"&RefId="+refid+"&Hiringdate="+hiring_date    
#        conn.request("POST", "/api/cz/UpdateApplicantStatus?IsEgyption=true&RefId=15236555&Hiringdate=2017-08-01", payload, headers)
#        res = conn.getresponse()
#        data = res.read()
#        print(data.decode("utf-8"))
        
