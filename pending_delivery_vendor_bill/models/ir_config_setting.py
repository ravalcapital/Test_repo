# -*- coding: utf-8 -*-

from odoo import fields, models


class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    vendor_journal_id = fields.Many2one('account.journal', string='Vendor Journal',
                                        config_parameter='stock_move_invoice.vendor_journal_id')