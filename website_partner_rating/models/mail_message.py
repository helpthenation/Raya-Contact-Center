# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details. 

from odoo import models, fields, api, _

class mailmessage(models.Model):
    _inherit='mail.message'
    
    message_rate = fields.Integer( 'Message Rating' )
    short_description = fields.Char( 'Short Description' )
    website_message = fields.Boolean( 'Is Website Message', default=False )
class Skills(models.Model):
    _name = "website.skills"
    
    skill_rate=fields.Integer('Skill Level')
    skill_description =fields.Char('Skill')
    partner_id = fields.Many2one('Partner')
    website_message = fields.Boolean( 'Is Website Message', default=False )
 