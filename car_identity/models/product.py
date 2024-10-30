# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_damage = fields.Boolean(string="Is Damage")

