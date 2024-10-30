# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    car_identity_id = fields.Many2one('car.identity', 'Car Identity')
