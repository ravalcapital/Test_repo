# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class FleetPriceList(models.Model):
    _name = 'fleet.price.list'
    _description = 'Fleet Price List'

    price_date = fields.Date(string='Date')
    price = fields.Integer(string='Price')
    model_id = fields.Many2one('fleet.vehicle.model', 'Models')
