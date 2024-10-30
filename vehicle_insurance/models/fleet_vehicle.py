# -*- coding: utf-8 -*-

from odoo import models


class FleetVehicleInherit(models.Model):
    _inherit = "fleet.vehicle"

    def name_get(self):
        result = []
        for vehicle in self:
            result.append((vehicle.id, "[%s] - %s" % (vehicle.vin_sn, vehicle.name)))
        return result
