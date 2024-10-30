# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PartnerLoan(models.Model):
    _inherit = 'partner.loan.details'

    term_change_loan_ids = fields.One2many(
        'term.change.history',
        'loan_id',
        string='Term Change History',
        copy=False,
    )
    allow_to_change_loan_term = fields.Boolean(
        'Allowed to Loan Change Term',
        related="loan_type.allow_to_change_loan_term",
        stored=True,
    )
    is_loan_term_changed = fields.Boolean(
        string='Is Loan Term Changed',
        copy=False,
    )

    @api.depends('installment_lines', 'principal_amount', 'int_rate', 'duration', 'installment_lines.state')
    def _cal_amount_all(self):
        print(f'in loan_change_terms_installment - _cal_amount_all ')
        res = super(PartnerLoan, self)._cal_amount_all()
        for rec in self:
            # if rec.is_loan_term_changed and rec.installment_lines:
            if rec.installment_lines:
                rec.total_interest_amount = 0.0
                rec.total_amount_paid = 0.0
                if rec.int_payable:
                    rec.total_interest_amount = round(sum(rec.installment_lines.mapped("interest_amt")))
                rec.total_amount_paid += round(sum(rec.installment_lines.filtered(lambda line:line.state == 'paid').mapped('total')))

                rec.final_total = rec.principal_amount + rec.total_interest_amount
                rec.total_amount_due= rec.final_total - rec.total_amount_paid


class PartnerLoanInstmntDetails(models.Model):
    _inherit = 'partner.loan.installment.details'
    
    active = fields.Boolean(
        string='Is Active',
        default=True,
    )

