# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class PendingDeliveryPayment(models.TransientModel):
    _name = 'pending.delivery.payment'
    _description = "Pending Delivery Payment"

    pending_delivery_id = fields.Many2one('pending.delivery', string="Pending Delivery")
    name = fields.Char(string="Origin", readonly=True)
    line_ids = fields.One2many('pending.payment.lines', 'pending_payment_id', string="Payment Lines")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)

    def gen_pending_delivery_payment(self):
        for line in self.line_ids:
            if line.amount == 0.00:
                raise ValidationError(_('Please enter valid payment amount..!'))

            payment_obj = self.env['account.payment']
            payment_data = {
                'payment_type': 'outbound',
                'partner_type': 'supplier',
                'partner_id': line.partner_id.id,
                'amount': line.amount,
                'journal_id': line.journal_id.id,
                'date': line.date,
                'ref': line.name,
                'payment_method_line_id': line.payment_method_id.id,
                'currency_id': line.currency_id.id,
                'company_id': line.company_id.id,
            }
            account_payment_id = payment_obj.create(payment_data)
            account_payment_id.pending_delivery_id = line.pending_delivery_id.id
            # account_payment_id.action_post()


class PendingPaymentLines(models.TransientModel):
    _name = 'pending.payment.lines'
    _description = 'Pending Payment Lines'

    pending_payment_id = fields.Many2one('pending.delivery.payment', string="Pending Delivery Payment")
    pending_delivery_id = fields.Many2one('pending.delivery', string="Pending Delivery",
                                          related="pending_payment_id.pending_delivery_id", store=True)
    journal_id = fields.Many2one('account.journal', string="Journal")
    partner_id = fields.Many2one('res.partner', string="Vendor")
    name = fields.Char(string="Memo")
    date = fields.Datetime(string="Date", default=fields.datetime.now())
    amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related="pending_payment_id.currency_id",
                                  store=True)
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', required=True)

    payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money')], string='Payment Type',
                                    default="outbound", required=True)

    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        if self.payment_type:
            return {'domain': {'payment_method_id': [('payment_type', '=', self.payment_type)]}}
