# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PartnerLoanType(models.Model):
    _inherit = 'partner.loan.type'

    allow_to_change_loan_term = fields.Boolean(
        'Allow to Change Term ?',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
