# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def submit_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'

    def submit_for_quotation_sent(self):
        for rec in self:
            rec.state = 'sent'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('waiting_for_approval', 'Waiting For Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sale Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
