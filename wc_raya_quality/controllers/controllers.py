# -*- coding: utf-8 -*-
# from odoo import http


# class WcRayaQuality(http.Controller):
#     @http.route('/wc_raya_quality/wc_raya_quality/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wc_raya_quality/wc_raya_quality/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wc_raya_quality.listing', {
#             'root': '/wc_raya_quality/wc_raya_quality',
#             'objects': http.request.env['wc_raya_quality.wc_raya_quality'].search([]),
#         })

#     @http.route('/wc_raya_quality/wc_raya_quality/objects/<model("wc_raya_quality.wc_raya_quality"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wc_raya_quality.object', {
#             'object': obj
#         })
