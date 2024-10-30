# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.addons.fleet.models.fleet_vehicle_model import FUEL_TYPES


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    maintenance_schedule_ids = fields.One2many('maintenance.schedule.plan', 'vehicle_id', string="Maintenance Plan")


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    maintenance_schedule_ids = fields.One2many('maintenance.schedule', 'model_id', string="Maintenance Schedule")
    price_list_ids = fields.One2many('fleet.price.list', 'model_id', string="Price List")

    def update_vehicle_maintenance_schedule_plan(self):
        for rec in self:
            vehicle_obj = self.env['fleet.vehicle'].search([('model_id', 'in', self.ids)])
            all_maintenance = []
            for vehicle in vehicle_obj:
                vehicle.maintenance_schedule_ids.unlink()
                for maintenance in rec.maintenance_schedule_ids:
                    plan_obj =self.env['maintenance.schedule.plan'].create({
                        'km_maintenance': maintenance.km_maintenance,
                        'vehicle_id': vehicle.id,
                        'model_id': maintenance.model_id.id,
                        'maintenance_schedule_id': maintenance.id,
                    })
                    all_maintenance.append(plan_obj.id)
                    print("sssss", all_maintenance)
