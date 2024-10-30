# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class VehicleLicense(models.Model):
    _name = "vehicle.license"
    _description = "Vehicle License"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    car_plate_no = fields.Char(string="Car Plate No.")
    license_years = fields.Char(string="License Years")
    license_start_date = fields.Date(string="License Start Date", track_visibility='onchange' )
    # license_probation_date = fields.Date(string="License Probation Date", track_visibility='onchange' )
    license_probation_date = fields.Date(string="Traffic Inspection Date", track_visibility='onchange' )
    license_renewal_date = fields.Date(string="License Renewal Date", track_visibility='onchange' )
    name = fields.Char(string="License Code", required=False,readonly=False )
    pending_delivery_id = fields.Many2one('pending.delivery', string="Pending Delivery")
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Car", required=False, )

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.license')
    #     return super(VehicleLicense, self).create(vals)
