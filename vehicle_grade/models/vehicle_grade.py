# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleGrade(models.Model):
    _name = 'vehicle.grade'
    _description = 'Vehicle Grade'

    name = fields.Char(string="Name", required=True)
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.company, readonly=True)
