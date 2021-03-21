# -*- coding: utf-8 -*-
# from odoo import http


# class WcTaQualification(http.Controller):
#     @http.route('/wc_ta_qualification/wc_ta_qualification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wc_ta_qualification/wc_ta_qualification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wc_ta_qualification.listing', {
#             'root': '/wc_ta_qualification/wc_ta_qualification',
#             'objects': http.request.env['wc_ta_qualification.wc_ta_qualification'].search([]),
#         })

#     @http.route('/wc_ta_qualification/wc_ta_qualification/objects/<model("wc_ta_qualification.wc_ta_qualification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wc_ta_qualification.object', {
#             'object': obj
#         })
