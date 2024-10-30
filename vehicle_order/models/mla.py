# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MlaData(models.Model):
    _inherit = 'mla.data'

    allowed_no_of_tire = fields.Integer(string="Allowed No Of Tire")

