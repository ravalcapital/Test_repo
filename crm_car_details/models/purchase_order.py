from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    color_id = fields.Many2one('crm.car.color')
    vehicle_model_id = fields.Many2one('fleet.vehicle.model.category')