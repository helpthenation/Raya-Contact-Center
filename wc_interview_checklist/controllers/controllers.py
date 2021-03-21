# -*- coding: utf-8 -*-
# from odoo import http


# class WcInterviewChecklist(http.Controller):
#     @http.route('/wc_interview_checklist/wc_interview_checklist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wc_interview_checklist/wc_interview_checklist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wc_interview_checklist.listing', {
#             'root': '/wc_interview_checklist/wc_interview_checklist',
#             'objects': http.request.env['wc_interview_checklist.wc_interview_checklist'].search([]),
#         })

#     @http.route('/wc_interview_checklist/wc_interview_checklist/objects/<model("wc_interview_checklist.wc_interview_checklist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wc_interview_checklist.object', {
#             'object': obj
#         })
