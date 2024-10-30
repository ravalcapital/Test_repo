# -*- coding: utf-8 -*-
# from odoo import http


# class VehicleNoTire(http.Controller):
#     @http.route('/vehicle_no_tire/vehicle_no_tire', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vehicle_no_tire/vehicle_no_tire/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vehicle_no_tire.listing', {
#             'root': '/vehicle_no_tire/vehicle_no_tire',
#             'objects': http.request.env['vehicle_no_tire.vehicle_no_tire'].search([]),
#         })

#     @http.route('/vehicle_no_tire/vehicle_no_tire/objects/<model("vehicle_no_tire.vehicle_no_tire"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vehicle_no_tire.object', {
#             'object': obj
#         })
