# -*- coding: utf-8 -*-
# from odoo import http


# class WcRayaUpdates2(http.Controller):
#     @http.route('/wc_raya_updates2/wc_raya_updates2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wc_raya_updates2/wc_raya_updates2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wc_raya_updates2.listing', {
#             'root': '/wc_raya_updates2/wc_raya_updates2',
#             'objects': http.request.env['wc_raya_updates2.wc_raya_updates2'].search([]),
#         })

#     @http.route('/wc_raya_updates2/wc_raya_updates2/objects/<model("wc_raya_updates2.wc_raya_updates2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wc_raya_updates2.object', {
#             'object': obj
#         })
