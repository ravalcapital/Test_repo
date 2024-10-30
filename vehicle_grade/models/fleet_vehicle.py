# -*- coding: utf-8 -*-

from odoo import models, fields


class FleetVehicleInherit(models.Model):
    _inherit = "fleet.vehicle"

    vehicle_grade_id = fields.Many2one('vehicle.grade', string='Vehicle Grade')

