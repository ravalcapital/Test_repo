# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class TermChangeHistory(models.Model):
    _name = 'term.change.history'
    _description = 'Loan Change Terms History'

    loan_id = fields.Many2one(
        'partner.loan.details',
        string='Loan',
    )
    term_change_date = fields.Datetime(
        string='Term Changed On',
    )
    term_change_by = fields.Many2one(
        'res.users',
        'Term Changed by',
    )
    old_duration = fields.Float(
        'Previous Duration (Months)'
    )
    new_duration = fields.Float(
        'New Duration (Months)'
    )
    old_int_rate = fields.Float(
        'Previous Interest Rate'
    )
    new_int_rate = fields.Float(
        'New Interest Rate'
    )
    old_start_installment_date = fields.Date(
        'Previous Starting Installment Date'
    )
    new_start_installment_date = fields.Date(
        'New Starting Installment Date'
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
