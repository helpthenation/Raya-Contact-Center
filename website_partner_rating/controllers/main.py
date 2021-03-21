# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import SUPERUSER_ID
import odoo.addons.website_partner_rating.controllers.main_p as website_partner_main
import werkzeug.urls
import werkzeug.wrappers
import json
import logging
from werkzeug.exceptions import Forbidden

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError


# class website_partner_rating_comments( website_partner_main.WebsiteCrmPartnerAssign ):
#     @http.route(['/partners/partner/comment/<int:partner_id>'], type='http', auth="public", methods=['POST'], website=True)
   
	# def partner_rating( self, partner_id, **post ):
	#     partner_obj = request.env['res.partner'].browse(partner_id)
	#     short_description = post.get( 'short_description' )
	#     review = post.get('review')
	#     comment = post.get('comment')

	#     if post.get( 'comment' ):
	#         reviews_ratings = partner_obj.message_post(
	#                                     body=post.get( 'comment' ),
	#                                     message_type='comment',
	#                                     subtype_xmlid='mail.mt_comment',
	#                                  )
			
	#         self.env['mail.message'].create({
	#                     'body': notes,
	#                     'model': 'account.bank.statement',
	#                     'res_id': self.cash_register_id.id,
	#                 })
			
	#         reviews_ratings = request.env['mail.message']
	#         # message_id1.write({'message_rate':review, 'short_description':short_description} )
	#         reviews_ratings.sudo().create({'message_rate':review, 'description':short_description})
	#         return werkzeug.utils.redirect( request.httprequest.referrer + "#comments" )


class website_partner_rating_comments( website_partner_main.WebsiteCrmPartnerAssign ):
    """ This method is overloaded for to add messaege_rate and short_description
    in product.template"""
    
    @http.route(['/partners/partner/delete/<int:message_id>'], type='http', auth="public", methods=['GET'], website=True)
    def partner_rating_delete( self,message_id, **post ):
        #skills_obj =  request.env['res.partner'].browse(partner_id)
        mail_message1 = request.env['website.skills'].search([('id','=',message_id)])
        mail_message1.unlink()
        return werkzeug.utils.redirect( request.httprequest.referrer + "#comments" )


    @http.route(['/partners/partner/comment/<int:partner_id>'], type='http', auth="public", methods=['POST'], website=True)
    def partner_rating( self, partner_id, **post ):
        partner_obj = request.env['res.partner'].browse(partner_id)
        #skills_obj =  request.env['res.partner'].browse(partner_id)
        if post.get( 'comment' ):
            message_id1 = partner_obj.message_post(
                body=post.get( 'comment' ),
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
             )

            review = post.get('review')
            short_description = post.get( 'skill_description' )
            mail_message1 = request.env['website.skills']
            mail_message1.create({'skill_rate':review, 
            					'skill_description':short_description, 
                                'partner_id':partner_id,
            					'website_message':True} )

            return werkzeug.utils.redirect( request.httprequest.referrer + "#comments" )


