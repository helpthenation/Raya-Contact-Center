# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from odoo.exceptions import ValidationError,UserError
import http.client
import json

class ISِAgency(models.Model):
    _inherit = 'res.partner'
    is_agency = fields.Boolean(string="Is Agency ")

class AgenciesData(models.Model):
    _name = 'agency.data'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    name= fields.Char(string="Agency Name")
    pin_code = fields.Char(string="Agency PIN Code")
    partner_id = fields.Many2one('res.partner',string="Related Partners")

class USERS(models.Model):
    _inherit = 'res.users'
    is_agency = fields.Boolean(string="Is Agency ")

class AgencyWizard(models.TransientModel):
    _name = "agency.import_wizard"
    _description= 'Agency Import Applications'
    
    
    agency = fields.Many2one('agency.data', string = "Select Your Agency")
    pin = fields.Char(string = "Enter your PIN Code")
    file = fields.Binary('File')
    
    def import_data(self):
        pass
    
