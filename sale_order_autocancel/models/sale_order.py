# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def autocancel_draft_sent_orders(self):
        days_default = 1
        limit_date = datetime.now() - timedelta(days=days_default)
        draft_sales = self.env['sale.order'].search(
            [('state', 'in', ['draft', 'sent', 'waiting_for_approval']), ('validity_date', '<=', limit_date)])
        for sale in draft_sales:
            sale.state = 'cancel'
