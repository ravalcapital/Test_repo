# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    repair_vb_id = fields.Many2one('repair.order', string='Repair Order')
    is_repair_order_bill = fields.Boolean(string='Is Repair Order Bill', copy=False)

