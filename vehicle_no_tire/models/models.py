# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class vehicle_no_tire(models.Model):
#     _name = 'vehicle_no_tire.vehicle_no_tire'
#     _description = 'vehicle_no_tire.vehicle_no_tire'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
