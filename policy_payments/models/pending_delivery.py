# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    payment_ids = fields.One2many('account.payment', 'pending_delivery_id', string="Payments", ondelete='restrict')
    payment_count = fields.Integer(compute="compute_payment_count")

    @api.depends('payment_ids')
    def compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    def action_view_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            "context": {"pending_delivery_id": self.id},
            'domain': [('id', 'in', self.mapped('payment_ids').ids)],
        }

    def create_payment(self):
        view_id = self.env.ref('policy_payments.pending_delivery_payment_wizard')
        if view_id:
            pay_wiz_data = {
                'name': _('Pending Delivery Payment'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pending.delivery.payment',
                'view_id': view_id.id,
                'target': 'new',
                'context': {
                    'name': self.name,
                    'pending_delivery_id': self.id,
                },
            }
            return pay_wiz_data


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    pending_delivery_id = fields.Many2one('pending.delivery', string="Pending Delivery")
