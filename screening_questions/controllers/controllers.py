# -*- coding: utf-8 -*-
# from odoo import http


# class ScreeningQuestions(http.Controller):
#     @http.route('/screening_questions/screening_questions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/screening_questions/screening_questions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('screening_questions.listing', {
#             'root': '/screening_questions/screening_questions',
#             'objects': http.request.env['screening_questions.screening_questions'].search([]),
#         })

#     @http.route('/screening_questions/screening_questions/objects/<model("screening_questions.screening_questions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('screening_questions.object', {
#             'object': obj
#         })
