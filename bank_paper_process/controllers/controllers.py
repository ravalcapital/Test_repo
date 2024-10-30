# -*- coding: utf-8 -*-
# from odoo import http


# class BankPaperProdcess(http.Controller):
#     @http.route('/bank_paper_prodcess/bank_paper_prodcess', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bank_paper_prodcess/bank_paper_prodcess/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bank_paper_prodcess.listing', {
#             'root': '/bank_paper_prodcess/bank_paper_prodcess',
#             'objects': http.request.env['bank_paper_prodcess.bank_paper_prodcess'].search([]),
#         })

#     @http.route('/bank_paper_prodcess/bank_paper_prodcess/objects/<model("bank_paper_prodcess.bank_paper_prodcess"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bank_paper_prodcess.object', {
#             'object': obj
#         })
