# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import werkzeug.urls

from collections import OrderedDict
from werkzeug.exceptions import NotFound

from odoo import fields
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_partner.controllers.main import WebsitePartnerPage

from odoo.tools.translate import _


class WebsiteAccount(CustomerPortal):
    # Create Language Skills
    @http.route(['/checkList'], type='http', auth="user", methods=['GET'],website=True)
    def portal_my_checklist(self, **post):
        is_emp = request.env['hr.employee'].sudo().search([('identification_id','=',request.env.user.partner_id.national_id)]).id
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        print(is_emp)
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        
        values = self._prepare_portal_layout_values()
        values.update({
            'is_emp': is_emp,
        })
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        return request.render("ow_portal.portal_check_list", values)
    #################################################################
    
    # My Non Technical Skills 
    @http.route(['/my/online'], type='http', auth="user", website=True)
    def portal_my_online(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'id': {'label': _('Newest'), 'order': 'id asc'}
        }

        # default sort by value
        if not sortby:
            sortby = 'id'
        order = searchbar_sortings[sortby]['order']
        is_emp = request.env['hr.employee'].sudo().search([('identification_id','=',request.env.user.partner_id.national_id)]).id
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        print(is_emp)
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        onboarding_onboarding = request.env['onboarding.onboarding'].sudo().search([('employee_id','=',is_emp),('stage_id','=',2)]).id
        domain = self.get_domain_my_online(onboarding_onboarding)
        
        if onboarding_onboarding:
            CrmLead = request.env['onboarding.online.share.clone.onboarding'].sudo().search([('onboard_onboarding_id','=',onboarding_onboarding)])
            entrylist = request.env['g.checklist.clone.onboarding'].sudo().search([('onboard_onboarding_id','=',onboarding_onboarding)],order='id')
            optionlist= request.env['onboarding.option.clone.onboarding'].sudo().search([('onboard_onboarding_id','=',onboarding_onboarding)],order='id')
            print("Option List")
            print("Option List")
            print("Option List")
            print(optionlist)
            print("Option List")
            print("Option List")
            
            lead_count = CrmLead.search_count(domain)
            pager = request.website.pager(
                url="/my/online",
                url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                total=lead_count,
                page=page,
                step=self._items_per_page
            )
            onlines = CrmLead.search(domain,order=order, limit=self._items_per_page, offset=pager['offset'])
            entrylist = entrylist.search(domain,order=order, limit=self._items_per_page, offset=pager['offset'])
            optionlist = optionlist.search(domain,order=order, limit=self._items_per_page, offset=pager['offset'])
            values.update({
                'date': date_begin,
                'onlines': onlines,
                'entrylist': entrylist,
                'optionlist':optionlist,
                'page_name': 'Online',
                'default_url': '/my/online',
                'pager': pager,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
               # 'skills_lst': skills_lst,
               # 'levels_lst':levels_lst,
            })
            
            
        else:
            onlines = request.env['onboarding.online.share.clone.onboarding'].sudo().search([('name','=','CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')])
            entrylist = request.env['g.checklist.clone.onboarding'].sudo().search([('name','=','CCCCCCCCCCCCCCCCCCCCCCCCCCCCC')],order='id')
            optionlist= request.env['onboarding.option.clone.onboarding'].sudo().search([('name','=','CCCCCCCCCCCCCCCCCCCCCCCCCCCCC')],order='id')
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print(is_emp)
        print(onboarding_onboarding)
        
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        
        
        #skills_type_obj = request.env['hr.skill.type'].sudo().search([('skill_type','=','non_technical')])
        #skills_lst = request.env['hr.skill'].sudo().search([('skill_type_id','=',skills_type_obj.id)])
        #levels_lst = request.env['hr.skill.level'].sudo().search([('skill_type_id','=',skills_type_obj.id)])

        

        #if date_begin and date_end:
        #    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # pager
        

        # content according to pager and archive selected
        
        
        
        return request.render("ow_portal.portal_my_online", values)
    
    ######                    Partners  Domains                  ####
    #################################################################
    def get_domain_my_online(self, user):
        return [
            ('onboard_onboarding_id', '=', user)
        ]
    
    def get_domain_my_lead(self, user):
        return [
            ('partner_non_tech_talent_id', '=', user.partner_id.id)
        ]
    
    def get_domain_my_opp(self, user):
        return [
            ('partner_tech_talent_id', '=', user.partner_id.id)
        ]

    def get_domain_my_lang(self, user):
        return [
            ('partner_lang_talent_id', '=', user.partner_id.id)
        ]
    
    #############################################################
    # Counters
    #############################################################
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)    
        # Non Tech Skills Counter
        
        if 'check_list_count' in counters:
            values['check_list_count'] = request.env['hr.skill.clone'].search_count(self.get_domain_my_lead(request.env.user))
            
        if 'skills_count' in counters:
            values['skills_count'] = request.env['hr.skill.clone'].search_count(self.get_domain_my_lead(request.env.user))
            
        # Non Tech Skills Counter
        if 'tec_skills_count' in counters:
            values['tec_skills_count'] = request.env['hr.skill.clone'].search_count(self.get_domain_my_opp(request.env.user))
        return values

        # Language Skills Counter
        if 'lang_skills_count' in counters:
            print("I am In")
            values['lang_skills_count'] = request.env['hr.skill.clone'].search_count([('partner_lang_talent_id', '=', request.env.user.partner_id.id)])
            print(request.env['hr.skill.clone'].search_count([('partner_lang_talent_id', '=', request.env.user.partner_id.id)]))
            print("I am In")
        return values


    @http.route(['/my/my/online/createg6'], type='http', auth="public", methods=['POST'],website=True)
    def updateG6(self, **post):
        is_emp = request.env['hr.employee'].sudo().search([('identification_id','=',request.env.user.partner_id.national_id)]).id
        onboarding_onboarding = request.env['onboarding.onboarding'].sudo().search([('employee_id','=',is_emp),('stage_id','=',2)]).id
        print("post")
        print(post)
        print("post")
        entrylist = request.env['g.checklist.clone.onboarding'].sudo().search([('onboard_onboarding_id','=',onboarding_onboarding)])
        new_data = "start transaction  "
        print("NNNNNNNNNNNNNNNNNNNNNNNNNN")

        control_id = ""
        print("NNNNNNNNNNNNNNNNNNNNNNNNNN")
        for ent in entrylist:
            control_id = str(ent.id)
            con = post.get(control_id)
            
            if con == 'on':
                con = "True"
            ent.write({'done':con})
        return request.redirect('/my/online')
    
    @http.route(['/my/my/online/options'], type='http', auth="public", methods=['POST'],website=True)
    def updateOp(self, **post):
        is_emp = request.env['hr.employee'].sudo().search([('identification_id','=',request.env.user.partner_id.national_id)]).id
        onboarding_onboarding = request.env['onboarding.onboarding'].sudo().search([('employee_id','=',is_emp),('stage_id','=',2)]).id
        
        print("post")
        print(post)
        print("post")
        #entrylist = request.env['entry.checklist.clone.onboarding'].sudo().search([('onboard_onboarding_id','=',onboarding_onboarding)])
        entrylist= request.env['onboarding.option.clone.onboarding'].sudo().search([('onboard_onboarding_id','=',onboarding_onboarding)])
        new_data = "start transaction  "
        print("NNNNNNNNNNNNNNNNNNNNNNNNNN")

        control_id = ""
        print("GBGFGBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        print("GBGFGBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        print("GBGFGBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        print("GBGFGBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        print("GBGFGBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        
        for ent in entrylist:
            control_id = str(ent.id)
            con = post.get(control_id)
            print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
            print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
            print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
            print(con)
            print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
            print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
            print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
            if con == 'on':
                con = "True"
                print("CONNNNNNNNNNNNNNNNNNNNNNNNN")
                ent.write({'select':con})
        return request.redirect('/my/online')
    
    # Create Language Skills
    @http.route(['/my/langskills/create'], type='http', auth="user", methods=['POST'],website=True)
    def portal_my_lang_skills_create(self, **post):
        skill_id = post.get('skill_id')
        lang_applicant_talent_level = post.get('lang_applicant_talent_level')
        partner_lang_talent_id	= request.env.user.partner_id.id
        mail_message1 = request.env['hr.skill.clone']
        mail_message1.create({'skill_id':skill_id,
                              'lang_applicant_talent_level':lang_applicant_talent_level,
                              'partner_lang_talent_id':partner_lang_talent_id,} )
        return request.redirect('/my/lang_skills')
        
    # Create Technical Skills
    @http.route(['/my/tec_skills/create'], type='http', auth="user", methods=['POST'],website=True)
    def portal_my_tech_skills_create(self, **post):
        skill_id = post.get('skill_id')
        tech_applicant_talent_level = post.get('tech_applicant_talent_level')
        partner_tech_talent_id	= request.env.user.partner_id.id
        mail_message1 = request.env['hr.skill.clone']
        mail_message1.create({'skill_id':skill_id,
                              'tech_applicant_talent_level':tech_applicant_talent_level,
                                'partner_tech_talent_id':partner_tech_talent_id,} )
        return request.redirect('/my/tec_skills')

    # Create Technical Skills
    @http.route(['/my/nonskills/create'], type='http', auth="user", methods=['POST'],website=True)
    def portal_my_skills_create(self, **post):
        skill_id = post.get('skill_id')
        nontech_applicant_talent_level = post.get('nontech_applicant_talent_level')
        partner_non_tech_talent_id	= request.env.user.partner_id.id
        mail_message1 = request.env['hr.skill.clone']
        mail_message1.create({'skill_id':skill_id,
                              'nontech_applicant_talent_level':nontech_applicant_talent_level,
                                'partner_non_tech_talent_id':partner_non_tech_talent_id,} )
        return request.redirect('/my/skills')
    
    
    
    # Delete Language Skills
    @http.route(['/my/lang_skills/delete/<int:message_id>'], type='http', auth="public", methods=['GET'], website=True)
    def lang_skills_delete( self,message_id, **post ):
        mail_message1 = request.env['hr.skill.clone'].search([('id','=',message_id)])
        mail_message1.unlink()
        return request.redirect('/my/lang_skills')
    
    # Delete Technical Skills
    @http.route(['/my/tec_skills/delete/<int:message_id>'], type='http', auth="public", methods=['GET'], website=True)
    def partner_rating_delete( self,message_id, **post ):
        mail_message1 = request.env['hr.skill.clone'].search([('id','=',message_id)])
        mail_message1.unlink()
        return request.redirect('/my/tec_skills')
    
    # Delete Non Technical Skills
    @http.route(['/my/non_skills/delete/<int:message_id>'], type='http', auth="public", methods=['GET'], website=True)
    def partner_rating_delete_nontech( self,message_id, **post ):
        mail_message1 = request.env['hr.skill.clone'].search([('id','=',message_id)])
        mail_message1.unlink()
        return request.redirect('/my/skills')
    
    
     # My check list
    @http.route(['/my/check_list', '/my/check_list/page/<int:page>'], type='http', auth="user", website=True)
    def portal_check_list(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        is_emp = request.env['hr.employee'].sudo().search([('identification_id','=',request.env.user.partner_id.national_id)]).id
        print("EMP")
        print("EMP")
        print(is_emp)
        print("EMP")
        print("EMP")
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['hr.skill.clone']
        domain = self.get_domain_my_lang(request.env.user)
        lead_count = CrmLead.search_count([('partner_lang_talent_id', '=', request.env.user.partner_id.id)])
        is_emp = request.env['hr.employee'].sudo().search([('identification_id','=',request.env.user.partner_id.national_id)]).id
        print("EMP")
        print("EMP")
        print(is_emp)
        print("EMP")
        print("EMP")
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'}
        }

        pager = request.website.pager(
            url="/my/check_list",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=lead_count,
            page=page,
            step=self._items_per_page
        )
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # content according to pager and archive selected
        skills = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'date': date_begin,
            'lang_skills': skills,
            'is_emp':is_emp,
            'page_name': 'Check List',
            'default_url': '/my/check_list',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        
        })
        return request.render("ow_portal.portal_my_check_list", values)
    
    
    # My Language Skills 
    @http.route(['/my/lang_skills', '/my/lang_skills/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_language(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['hr.skill.clone']
        domain = self.get_domain_my_lang(request.env.user)
        
        skills_type_obj = request.env['hr.skill.type'].sudo().search([('skill_type','=','language')])
        skills_lst = request.env['hr.skill'].sudo().search([('skill_type_id','=',skills_type_obj.id)])
        levels_lst = request.env['hr.skill.level'].sudo().search([('skill_type_id','=',skills_type_obj.id)])

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # pager
        lead_count = CrmLead.search_count([('partner_lang_talent_id', '=', request.env.user.partner_id.id)])
        print(lead_count)
        pager = request.website.pager(
            url="/my/lang_skills",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=lead_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        skills = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'lang_skills': skills,
            'page_name': 'language skills',
            'default_url': '/my/lang_skills',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'skills_lst': skills_lst,
            'levels_lst':levels_lst,
        })
        return request.render("ow_portal.portal_my_lang_skills", values)
    
    # My Non Technical Skills 
    @http.route(['/my/skills', '/my/skills/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_leads(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['hr.skill.clone']
        domain = self.get_domain_my_lead(request.env.user)
        
        skills_type_obj = request.env['hr.skill.type'].sudo().search([('skill_type','=','non_technical')])
        skills_lst = request.env['hr.skill'].sudo().search([('skill_type_id','=',skills_type_obj.id)])
        levels_lst = request.env['hr.skill.level'].sudo().search([('skill_type_id','=',skills_type_obj.id)])

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # pager
        lead_count = CrmLead.search_count(domain)
        pager = request.website.pager(
            url="/my/skills",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=lead_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        skills = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'skills': skills,
            'page_name': 'skills',
            'default_url': '/my/skills',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'skills_lst': skills_lst,
            'levels_lst':levels_lst,
        })
        return request.render("ow_portal.portal_my_skills", values)

    @http.route(['/my/tec_skills', '/my/tec_skills/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_opportunities(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['hr.skill.clone']
        domain = self.get_domain_my_opp(request.env.user)

        today = fields.Date.today()
        this_week_end_date = fields.Date.to_string(fields.Date.from_string(today) + datetime.timedelta(days=7))

        searchbar_filters = {
            'all': {'label': _('Active'), 'domain': []}
        }
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # pager
        opp_count = CrmLead.search_count(domain)
        pager = request.website.pager(
            url="/my/tec_skills",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=opp_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager
        tec_skills = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        skills_type_obj = request.env['hr.skill.type'].sudo().search([('skill_type','=','technical')])
        skills_lst = request.env['hr.skill'].sudo().search([('skill_type_id','=',skills_type_obj.id)])
        levels_lst = request.env['hr.skill.level'].sudo().search([('skill_type_id','=',skills_type_obj.id)])
        
        
        values.update({
            'date': date_begin,
            'tec_skills': tec_skills,
            'page_name': 'tec_skill',
            'default_url': '/my/tec_skills',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'skills_lst': skills_lst,
            'levels_lst':levels_lst,
        })
        return request.render("ow_portal.portal_my_tec_skills", values)
    
    #Show Skills 
    @http.route(['''/my/lang_skills/<model('hr.skill.clone'):lang_skill>'''], type='http', auth="user", website=True)
    def portal_my_lang(self, lang_skill, **kw):
        return request.render("ow_portal.portal_my_lang_skill", {'lang_skill': lang_skill})

    @http.route(['''/my/skills/<model('hr.skill.clone'):skill>'''], type='http', auth="user", website=True)
    def portal_my_lead(self, skill, **kw):
        return request.render("ow_portal.portal_my_skill", {'skill': skill})

    @http.route(['''/my/tec_skills/<model('hr.skill.clone'):tec_skill>'''], type='http', auth="user", website=True)
    def portal_my_opportunity(self, tec_skill, **kw):
        return request.render(
            "ow_portal.portal_my_tec_skills", {
                'tec_skill': tec_skill
                #'user_activity': opp.sudo().activity_ids.filtered(lambda activity: activity.user_id == request.env.user)[:1],
                #'stages': request.env['crm.stage'].search([('is_won', '!=', True)], order='sequence desc, name desc, id desc'),
                #'activity_types': request.env['mail.activity.type'].sudo().search([]),
                #'states': request.env['res.country.state'].sudo().search([]),
                #'countries': request.env['res.country'].sudo().search([]),
            })

