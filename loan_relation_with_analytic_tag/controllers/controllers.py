# -*- coding: utf-8 -*-
# from odoo import http


# class LoanRelationWithAnalyticTag(http.Controller):
#     @http.route('/loan_relation_with_analytic_tag/loan_relation_with_analytic_tag', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/loan_relation_with_analytic_tag/loan_relation_with_analytic_tag/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('loan_relation_with_analytic_tag.listing', {
#             'root': '/loan_relation_with_analytic_tag/loan_relation_with_analytic_tag',
#             'objects': http.request.env['loan_relation_with_analytic_tag.loan_relation_with_analytic_tag'].search([]),
#         })

#     @http.route('/loan_relation_with_analytic_tag/loan_relation_with_analytic_tag/objects/<model("loan_relation_with_analytic_tag.loan_relation_with_analytic_tag"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('loan_relation_with_analytic_tag.object', {
#             'object': obj
#         })
