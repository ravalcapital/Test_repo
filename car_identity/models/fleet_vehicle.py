# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.addons.fleet.models.fleet_vehicle_model import FUEL_TYPES


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    car_identity_id = fields.Many2one('car.identity', 'Car Identity')
