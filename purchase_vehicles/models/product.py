# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_vehicle = fields.Boolean(string="Is Vehicle")
    split_delivery = fields.Boolean(string="Split Delivery")
    split_receipt = fields.Boolean(string="Pending Delivery")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_vehicle = fields.Boolean(string="Is Vehicle")
    split_delivery = fields.Boolean(string="Split Delivery")
    split_receipt = fields.Boolean(string="Pending Delivery")

