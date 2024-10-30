# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    extra_km = fields.Boolean(string="Extra KM")
    tire = fields.Boolean(string="Tire")

