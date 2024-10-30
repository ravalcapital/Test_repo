# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pending_delivery_bills = fields.Boolean(string="Pending Delivery Bills")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pending_delivery_vendor = fields.Boolean(string="Pending Delivery Vendor")
