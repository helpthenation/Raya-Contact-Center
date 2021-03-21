# -*- coding: utf-8 -*-
# from odoo import http


# class InterviewFeedback(http.Controller):
#     @http.route('/interview_feedback/interview_feedback/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/interview_feedback/interview_feedback/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('interview_feedback.listing', {
#             'root': '/interview_feedback/interview_feedback',
#             'objects': http.request.env['interview_feedback.interview_feedback'].search([]),
#         })

#     @http.route('/interview_feedback/interview_feedback/objects/<model("interview_feedback.interview_feedback"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('interview_feedback.object', {
#             'object': obj
#         })
