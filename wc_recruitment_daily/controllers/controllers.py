# -*- coding: utf-8 -*-
# from odoo import http


# class WcRayaQoh(http.Controller):
#     @http.route('/wc_raya_qoh/wc_raya_qoh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wc_raya_qoh/wc_raya_qoh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wc_raya_qoh.listing', {
#             'root': '/wc_raya_qoh/wc_raya_qoh',
#             'objects': http.request.env['wc_raya_qoh.wc_raya_qoh'].search([]),
#         })

#     @http.route('/wc_raya_qoh/wc_raya_qoh/objects/<model("wc_raya_qoh.wc_raya_qoh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wc_raya_qoh.object', {
#             'object': obj
#         })
