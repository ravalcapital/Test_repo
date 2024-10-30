# -*- coding: utf-8 -*-

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError, ValidationError


class PartnerLoanType(models.Model):
    _inherit = 'partner.loan.type'

    interest_mode = fields.Selection(selection_add=[('fixed_principal', "Fixed Principal")],
                                     ondelete={'fixed_principal': 'set null'})


class PartnerLoanDetails(models.Model):
    _inherit = 'partner.loan.details'

    interest_mode = fields.Selection(selection_add=[('fixed_principal', "Fixed Principal")],
                                     ondelete={'fixed_principal': 'set null'})
    interest_code = fields.Char(related='loan_type.code',store=True,copy=False)
    @api.model
    def create_installments(self, loan):
        date_approved = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        if not loan.date_disb:
            raise ValidationError(_('Please give disbursement date.'))
        else:
            date_disb = loan.date_disb
        date_approved_obj = datetime.strptime(str(date_disb), DEFAULT_SERVER_DATE_FORMAT)
        installment_obj = self.env['partner.loan.installment.details']
        day = date_approved_obj.day
        month = date_approved_obj.month
        year = date_approved_obj.year
        beginning_balance = 0.0
        ending_balance = 0.0
        interest_amt = 0.0
        principal_amt = loan.principal_amount / (loan.duration or 1.0)
        if loan.int_payable:
            interest_amt = loan.total_interest_amount / (loan.duration or 1.0)
        total = principal_amt + interest_amt
        if loan.interest_mode == 'reducing':
            if loan.int_rate > 0.0:
                reducing_val = self.reducing_balance_method(loan.principal_amount, loan.int_rate, loan.duration)
        for install_no in range(0, loan.duration):
            date_from, date_to = self._get_installment_dates(year, month, day)
            #            date_from = datetime(year, month, day)
            #            date_to = date_from + relativedelta(months=1)
            if loan.interest_mode == 'reducing':
                if loan.int_rate > 0.0:
                    principal_amt = reducing_val[install_no]['principal_comp']
                #                if loan.int_payable:
                if loan.int_payable and loan.int_rate > 0.0:
                    interest_amt = reducing_val[install_no]['interest_comp']
                total = principal_amt + interest_amt
            if loan.interest_mode == 'mortgage_loan':
                if install_no > 0:
                    beginning_balance = ending_balance
                else:
                    beginning_balance = loan.principal_amount
                if loan.int_rate > 0.0:
                    total = (loan.principal_amount * ((loan.int_rate / 100) / loan.duration)) / (
                                1 - ((1 + ((loan.int_rate / 100) / loan.duration)) ** - loan.duration))
                    interest_amt = round((((loan.int_rate / 100) / loan.duration) * beginning_balance), 2)
                    principal_amt = round((total - interest_amt), 2)
                    ending_balance = round((beginning_balance - total), 2)
            if loan.interest_mode == 'fixed_principal':
                if install_no > 0:
                    beginning_balance = ending_balance
                else:
                    beginning_balance = loan.principal_amount
                principal_amt = round((loan.principal_amount / loan.duration), 2)
                if loan.int_rate > 0.0:
                    interest_amt = round(((beginning_balance * (loan.int_rate / 100)) / 12), 2)
                total = round((principal_amt + interest_amt), 2)
                ending_balance = round((beginning_balance - principal_amt), 2)

            day, month, year = date_to.day, date_to.month, date_to.year
            installment_line = {'install_no': install_no + 1,
                                'date_from': date_from.strftime('%Y-%m-%d'),
                                'date_to': date_to.strftime('%Y-%m-%d'),
                                'beginning_balance': beginning_balance,
                                'ending_balance': ending_balance,
                                'principal_amt': principal_amt,
                                'interest_amt': interest_amt,
                                'total': total,
                                'loan_id': loan.id,
                                'bank_journal_id': loan.bank_journal_id_for_int.id,
                                }
            installment_obj.create(installment_line)
        return True

    def compute_installments(self):
        for loan in self:
            if not len(loan.installment_lines):
                self.create_installments(loan)
            elif self._context.get('recompute') and loan.int_payable:
                access_payment = 0.0
                duration_left = 0
                prin_amt_received = 0.0
                total_acc_pay = 0.0
                for install in loan.installment_lines:
                    access_payment += round(install.total - (install.principal_amt + install.interest_amt), 2)
                    if install.state in ('paid', 'approve'):
                        prin_amt_received += round(install.principal_amt, 2)
                        continue
                    duration_left += 1
                total_acc_pay = loan.duration - duration_left
                new_p = round(loan.principal_amount - round(prin_amt_received, 2) - round(access_payment, 2))
                if loan.interest_mode == 'reducing':
                    if loan.int_rate > 0:
                        reducing_val = self.reducing_balance_method(new_p, loan.int_rate, duration_left)
                if loan.interest_mode == 'flat':
                    interest_amt = 0.0
                    principal_amt = new_p / duration_left
                    if loan.int_payable:
                        interest_amt = self.flat_rate_method(new_p, loan.int_rate, duration_left) / duration_left
                    total = principal_amt + interest_amt

                cnt = -1
                for install in loan.installment_lines:
                    cnt += 1
                    if install.state in ('paid', 'approve'): continue
                    if loan.interest_mode == 'reducing':
                        principal_amt = reducing_val[cnt - total_acc_pay]['principal_comp']
                        if loan.int_payable:
                            interest_amt = reducing_val[cnt - total_acc_pay]['interest_comp']
                        total = principal_amt + interest_amt
                    beginning_balance = 0.0
                    ending_balance = 0.0
                    if loan.interest_mode == 'mortgage_loan':
                        if cnt > 1:
                            beginning_balance = ending_balance
                        else:
                            beginning_balance = loan.principal_amount
                        if loan.int_rate > 0.0:
                            total = (loan.principal_amount * ((loan.int_rate / 100) / loan.duration)) / (
                                    1 - ((1 + ((loan.int_rate / 100) / loan.duration)) ** - loan.duration))
                            interest_amt = round((((loan.int_rate / 100) / loan.duration) * beginning_balance), 2)
                            principal_amt = round((total - interest_amt), 2)
                            ending_balance = round((beginning_balance - total), 2)
                    if loan.interest_mode == 'fixed_principal':
                        if cnt > 0:
                            beginning_balance = ending_balance
                        else:
                            beginning_balance = loan.principal_amount
                        principal_amt = round((loan.principal_amount / loan.duration), 2)
                        if loan.int_rate > 0.0:
                            interest_amt = round(((beginning_balance * (loan.int_rate / 100)) / 12), 2)
                        total = round((principal_amt + interest_amt), 2)
                        ending_balance = round((beginning_balance - principal_amt), 2)

                    install.write({'principal_amt': principal_amt,
                                   'beginning_balance': beginning_balance,
                                   'interest_amt': interest_amt,
                                   'ending_balance': ending_balance,
                                   'total': total})
            else:
                # this is to reload the values
                loan.write({})
                for install in loan.installment_lines:
                    install.write({})
        return True

    def recalc_installement_loan(self):
        for loan in self:
            if loan.interest_mode == 'fixed_principal' and loan.int_payable and loan.loan_type.code == 'AH FX':
                principal_amount = loan.principal_amount
                duration = loan.duration
                for line in loan.installment_lines:
                    line.total = round(principal_amount/duration,2)
                    line.principal_amt = line.total - line.interest_amt
    def recalculate_alhaly_loan(self):
        for rec in self:
            if rec.loan_type.code =='AH FX':
                rec.recalc_installement_loan()
