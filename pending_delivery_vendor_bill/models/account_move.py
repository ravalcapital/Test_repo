# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    pending_delivery_id = fields.Many2one('pending.delivery', string='Pending Delivery')
    is_pending_delivery_bill = fields.Boolean(string='Is Pending Delivery Bill', copy=False)

    applied_partner_ids = fields.Many2many('res.partner', compute='_get_partner_ids')

    @api.depends('is_pending_delivery_bill', 'pending_delivery_id')
    def _get_partner_ids(self):
        for move in self:
            if move.pending_delivery_id and move.is_pending_delivery_bill == True:
                move.applied_partner_ids = [
                    [6, 0, [p.id for p in
                            self.env['res.partner'].sudo().search(
                                [('pending_delivery_vendor', '=', True),
                                 ('company_id', 'in', [move.company_id.id, False])])]]]
            else:
                move.applied_partner_ids = [
                    [6, 0, [p.id for p in self.env['res.partner'].sudo().search(
                        [('company_id', 'in', [move.company_id.id, False])])]]]


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    applied_product_ids = fields.Many2many('product.product', compute='_get_product_ids')

    @api.depends('move_id.is_pending_delivery_bill', 'move_id.pending_delivery_id')
    def _get_product_ids(self):
        for line in self:
            if line.move_id.pending_delivery_id and line.move_id.is_pending_delivery_bill == True:
                line.applied_product_ids = [
                    [6, 0, [p.id for p in
                            self.env['product.product'].sudo().search(
                                ['|', ('sale_ok', '=', True), ('purchase_ok', '=', True),
                                 ('company_id', 'in', [line.company_id.id, False]),
                                 ('pending_delivery_bills', '=', True)])]]]
            else:
                line.applied_product_ids = [
                    [6, 0, [p.id for p in self.env['product.product'].sudo().search(
                        ['|', ('sale_ok', '=', True), ('purchase_ok', '=', True),
                         ('company_id', 'in', [line.company_id.id, False])])]]]
