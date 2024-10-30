# -*- coding: utf-8 -*-
# from odoo import http


# class FleetPo(http.Controller):
#     @http.route('/fleet_po/fleet_po/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fleet_po/fleet_po/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fleet_po.listing', {
#             'root': '/fleet_po/fleet_po',
#             'objects': http.request.env['fleet_po.fleet_po'].search([]),
#         })

#     @http.route('/fleet_po/fleet_po/objects/<model("fleet_po.fleet_po"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fleet_po.object', {
#             'object': obj
#         })
