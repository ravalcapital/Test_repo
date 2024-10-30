# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    car_identity_id = fields.Many2one('car.identity', related="purchase_line_id.car_identity_id", store=True,
                                      string='Car Identity')

    def action_create_vehicle(self):
        res= super(PendingDelivery, self).action_create_vehicle()
        if self.vehicle_id:
            self.vehicle_id.car_identity_id = self.car_identity_id.id
        return res
