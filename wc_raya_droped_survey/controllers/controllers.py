# -*- coding: utf-8 -*-
# from odoo import http


# class WcRayaDropedSurvey(http.Controller):
#     @http.route('/wc_raya_droped_survey/wc_raya_droped_survey/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wc_raya_droped_survey/wc_raya_droped_survey/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wc_raya_droped_survey.listing', {
#             'root': '/wc_raya_droped_survey/wc_raya_droped_survey',
#             'objects': http.request.env['wc_raya_droped_survey.wc_raya_droped_survey'].search([]),
#         })

#     @http.route('/wc_raya_droped_survey/wc_raya_droped_survey/objects/<model("wc_raya_droped_survey.wc_raya_droped_survey"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wc_raya_droped_survey.object', {
#             'object': obj
#         })
