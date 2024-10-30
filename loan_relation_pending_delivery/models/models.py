# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerLoanDetails(models.Model):
    _inherit = 'partner.loan.details'

    pending_delivery_ids = fields.Many2many('pending.delivery', ondelete='restrict')

    principal_amount = fields.Float(string='Principal Amount', required=True)

    @api.onchange('pending_delivery_ids', 'pending_delivery_ids.bank_loan_amount')
    def get_pricipal_amount(self):
        for rec in self:
            principal_amount = 0
            for pl in rec.pending_delivery_ids:
                principal_amount += pl.bank_loan_amount
            rec.principal_amount = principal_amount

    # principal_amount = fields.Float(
    #     string='Principal Amount',
    #     required=True,
    #     readonly=True,
    #     compute='get_pricipal_amount',
    #     store=True
    # )
    #
    # @api.depends('pending_delivery_ids.bank_loan_amount')
    # def get_pricipal_amount(self):
    #     for rec in self:
    #         principal_amount = 0
    #         for pl in rec.pending_delivery_ids:
    #             principal_amount += pl.bank_loan_amount
    #         rec.principal_amount = principal_amount
