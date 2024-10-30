# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class UpdateLoanInstallment(models.Model):
    _name = 'change.loan.term.installment'
    _description = 'Loan Term Change'

    duration = fields.Integer(
        string='Update Duration (Months)',
    )
    interest_rate = fields.Float(
        string='Update Interest Rate',
    )
    next_instment_date = fields.Date(
        string='Next Installment Start From',
    )
    is_change_next_intmnt_date = fields.Boolean(
        string='Change Next Installment Date',
    )
    is_change_duration = fields.Boolean(
        string='Change Duration',
    )
    is_change_int_rate = fields.Boolean(
        string='Change Interest Rate'
    )
    is_confirm_change_term = fields.Boolean(
        string='Are you sure you want to Chang Terms ?',
    )

    def _prepare_term_change_history_vals(self, loan_ids, term_change_history_vals):
        term_change_history_vals.update({
            'loan_id': loan_ids.id,
            'term_change_date' : fields.Datetime.now(),
            'term_change_by' : self.env.user.id,
            'new_duration' : self.duration or loan_ids.duration,
            'new_int_rate' : self.interest_rate or loan_ids.int_rate,
        })
        return term_change_history_vals

    # def _get_installment_values(self, loan, duration, paid_installment_line_ids):
    #     principal_amt = loan.principal_amount - sum(paid_installment_line_ids.mapped("principal_amt"))
    #     interest_amt = total = 0.0
    #     reducing_val = {}
    #     loan_principal_amnt = principal_amt
    #     if loan.int_payable:
    #         interest_rate = self.interest_rate or loan.int_rate or 0.0
    #         if loan.interest_mode == 'flat':
    #             principal_amt = loan_principal_amnt / (duration - len(paid_installment_line_ids) or 1.0)
    #             total_interest_amount = loan.flat_rate_method(loan_principal_amnt, interest_rate, duration - len(paid_installment_line_ids))
    #             interest_amt = total_interest_amount / (duration - len(paid_installment_line_ids) or 1.0)
    #             total = principal_amt + interest_amt
    #         if loan.interest_mode == 'reducing':
    #             if interest_rate > 0.0:
    #                 reducing_val = loan.reducing_balance_method(loan_principal_amnt, interest_rate, duration - len(paid_installment_line_ids))
    #         # =========================== new code for Fixed Principal ================
    #
    #         if loan.interest_mode == 'fixed_principal':
    #             cnt = -1
    #             principal_amt = 0.0
    #             beginning_balance = 0.0
    #             ending_balance = 0.0
    #             interest_amt = 0.0
    #             total = 0.0
    #             for install in loan.installment_lines:
    #                 cnt += 1
    #                 if install.state in ('paid', 'approve'): continue
    #
    #                 if loan.interest_mode == 'fixed_principal':
    #                     if cnt > 0:
    #                         beginning_balance = ending_balance
    #                     else:
    #                         beginning_balance = loan.principal_amount
    #                     principal_amt = round((loan.principal_amount / loan.duration), 2)
    #                     interest_amt = round(((beginning_balance * (loan.int_rate / 100)) / 12), 2)
    #                     print(f'in fixed_principal loan.int_rate > 0.0 - beginning_balance :{beginning_balance} -  - loan.int_rate:{loan.int_rate} - interest_amt:{interest_amt} ')
    #                     total = round((principal_amt + interest_amt), 2)
    #                     ending_balance = round((beginning_balance - principal_amt), 2)
    #
    #                     install.write({'principal_amt': principal_amt,
    #                                    'beginning_balance': beginning_balance,
    #                                    'interest_amt': interest_amt,
    #                                    'ending_balance': ending_balance,
    #                                    'total': total})
    #
    #         # =========================== End new code for Fixed Principal ============
    #         print(f'in _get_installment_values -  vals before return - principal_amt:{principal_amt} - interest_amt:{interest_amt} - total:{total} - reducing_val:{reducing_val}')
    #     return principal_amt, interest_amt, total, reducing_val

    def _get_installment_values(self, loan, duration, paid_installment_line_ids):
        print(f'in _get_installment_values - self:{self} - loan :{loan} -  duration :{duration} - paid_installment_line_ids :{paid_installment_line_ids}')
        principal_amt = loan.principal_amount - sum(paid_installment_line_ids.mapped("principal_amt"))
        interest_amt = total = 0.0
        reducing_val = {}
        loan_principal_amnt = principal_amt
        if loan.int_payable:
            interest_rate = self.interest_rate or loan.int_rate or 0.0
            if loan.interest_mode == 'flat':
                principal_amt = loan_principal_amnt / (duration - len(paid_installment_line_ids) or 1.0)
                total_interest_amount = loan.flat_rate_method(loan_principal_amnt, interest_rate, duration - len(paid_installment_line_ids))
                interest_amt = total_interest_amount / (duration - len(paid_installment_line_ids) or 1.0)
                total = principal_amt + interest_amt
            if loan.interest_mode == 'reducing':
                if interest_rate > 0.0:
                    reducing_val = loan.reducing_balance_method(loan_principal_amnt, interest_rate, duration - len(paid_installment_line_ids))
            # =========================== new code for Fixed Principal ================

            if loan.interest_mode == 'fixed_principal':
                cnt = -1
                principal_amt = 0.0
                beginning_balance = 0.0
                ending_balance = 0.0
                interest_amt = 0.0
                total = 0.0
                installment_paid = loan.installment_lines.search_count([('state','=','paid')])
                print(f'in _get_installment_values - installment_paid:{installment_paid}')
                installment_paid2 = loan.installment_lines.filtered(lambda i: i.state in ['paid','approve','booked'])
                print(f'in _get_installment_values - installment_paid2:{installment_paid2}')
                installment_paid2_ordered = installment_paid2.sorted(lambda o: o.install_no,reverse=True)
                print(f'in _get_installment_values - installment_paid2_ordered:{installment_paid2_ordered}')
                for install in loan.installment_lines:
                    cnt += 1
                    if install.state in ('paid', 'approve','booked'): continue

                    if loan.interest_mode == 'fixed_principal':
                        # if cnt > 0:
                        if cnt > 0:
                            # if install.id ==installment_paid2_ordered[0].id+1:
                            #     print(f'hhhhhhhhhhhhhhhhhhhhhhh')
                            if installment_paid2_ordered:
                                if install.install_no ==installment_paid2_ordered[0].install_no+1:
                                    print(f'hhhhhhhhhhhhhhhhhhhhhhh333333333333')
                                    beginning_balance = installment_paid2_ordered[0].ending_balance
                                else:
                                    beginning_balance = ending_balance
                            else:
                                print(
                                    f'in elseee - no installment_paid2_ordered kkkk - installment_paid2_ordered:{installment_paid2_ordered} - ending_balance :{ending_balance} - beginning_balance :{beginning_balance}')
                                beginning_balance = ending_balance
                                # interest_amt = round(((beginning_balance * (loan.int_rate / 100)) / 12), 2)
                                # print(
                                #     f'in elseee - no installment_paid2_ordered afttttt - installment_paid2_ordered:{installment_paid2_ordered} - ending_balance :{ending_balance} - beginning_balance :{beginning_balance} - interest_amt:{interest_amt}')
                                # continue
                        else:
                            beginning_balance = loan.principal_amount
                        principal_amt = round((loan.principal_amount / loan.duration), 2)
                        interest_amt = round(((beginning_balance * (loan.int_rate / 100)) / 12), 2)
                        print(f'in fixed_principal loan.int_rate > 0.0 - beginning_balance :{beginning_balance} -  - loan.int_rate:{loan.int_rate} - interest_amt:{interest_amt} ')
                        print(f'case installment_paid2_ordered :{installment_paid2_ordered} - len(installment_paid2_ordered)- : {len(installment_paid2_ordered)} - loan.duration:{loan.duration}')
                        print(f'in fixed_principal loan.int_rate > 0.0 - loan.principal_amount :{loan.principal_amount} -  - beginning_balance:{beginning_balance} - - loan.int_rate :{loan.int_rate} - loan.duration:{loan.duration} ')
                        total = round((principal_amt + interest_amt), 2)
                        ending_balance = round((beginning_balance - principal_amt), 2)

                        install.write({'principal_amt': principal_amt,
                                       'beginning_balance': beginning_balance,
                                       'interest_amt': interest_amt,
                                       'ending_balance': ending_balance,
                                       'total': total})

            # =========================== End new code for Fixed Principal ============
            print(f'in _get_installment_values -  vals before return - principal_amt:{principal_amt} - interest_amt:{interest_amt} - total:{total} - reducing_val:{reducing_val}')
        return principal_amt, interest_amt, total, reducing_val

    def _get_next_installment_dates(self, loan, year, month, day):
        date_from = datetime(year, month, day)
        date_to = date_from + relativedelta(months=1)
        return date_from, date_to

    def _get_new_installment_dates(self, loan, date_from):
        date_to = date_from + relativedelta(months=1)
        return date_from, date_to

#     def update_installments(self, loan, term_change_history_vals):
#         installment_obj = self.env['partner.loan.installment.details']
#         hidden_installment_line_ids = installment_obj.search([('active', '=', False), ('loan_id', '=', loan.id)], order='install_no')
#         installment_line_ids = loan.installment_lines.filtered(lambda instlmnt:instlmnt.state != 'paid')
#         installment_line_ids += hidden_installment_line_ids
#         paid_installment_line_ids = loan.installment_lines.filtered(lambda instlmnt:instlmnt.state == 'paid')
#         if self.next_instment_date:
#             date_disb = self.next_instment_date
#
#             day = date_disb.day
#             month = date_disb.month
#             year = date_disb.year
#
#             term_change_history_vals.update({
#                 'old_start_installment_date': installment_line_ids[0].date_from,
#                 'new_start_installment_date': self.next_instment_date,
#             })
#         duration = self.duration or loan.duration
#         interest_rate = self.interest_rate or loan.int_rate or 0.0
#         if self.is_change_duration or self.is_change_int_rate:
#             principal_amt, interest_amt, total, reducing_val = self._get_installment_values(loan, duration, paid_installment_line_ids)
#             print(f'in update_installments - principal_amt  {principal_amt} - interest_amt:{interest_amt}- total:{total} - reducing_val:{reducing_val}')
#
#         install_no = installment_line_ids[0].install_no
#         inst_mnt = installment_line_ids[0]
#         reduce_val_inst_no = 0
#         #inst_mnt_date = installment_line_ids[0].date_from
#         for install_mnt in installment_line_ids:
#             if duration < install_no:
#                 install_mnt.write({
#                     'active': False,
#                 })
#                 continue
#             install_mnt_vals = {}
#             if self.next_instment_date:
# #                date_from = datetime(year, month, day)
# #                date_to = date_from + relativedelta(months=1)
#                 date_from, date_to = self._get_next_installment_dates(loan, year, month, day)
#                 install_mnt_vals.update({
#                     'date_from':date_from.strftime('%Y-%m-%d'),
#                     'date_to':date_to.strftime('%Y-%m-%d'),
#                 })
#                 day, month, year = date_to.day, date_to.month, date_to.year
#             if self.is_change_duration or self.is_change_int_rate:
#                 print(f'in update_installments - in is_change_int_rate ')
#                 if loan.interest_mode == 'reducing':
#                     if interest_rate > 0.0:
#                         principal_amt = reducing_val[reduce_val_inst_no]['principal_comp']
#                     if loan.int_payable and interest_rate > 0.0:
#                         interest_amt = reducing_val[reduce_val_inst_no]['interest_comp']
#                     total = principal_amt + interest_amt
#                 install_mnt_vals.update({
#                     'active': True,
#                     'principal_amt':principal_amt,
#                     'interest_amt':interest_amt,
#                     'total':total,
#                     'loan_id':loan.id
#                 })
#             if install_mnt_vals:
#                 print(f'in update_installments - install_mnt_vals:{install_mnt_vals} ')
#                 install_mnt.write(install_mnt_vals)
#             inst_mnt = install_mnt
#             install_no += 1
#             reduce_val_inst_no += 1
#
#         if duration > inst_mnt.install_no:
#             date_from = inst_mnt.date_to
# #            date_to = inst_mnt.date_to + relativedelta(months=1)
#             date_from, date_to = self._get_new_installment_dates(loan, date_from)
#             for installment_no in range(inst_mnt.install_no, duration):
#                 if loan.interest_mode == 'reducing':
#                     if interest_rate > 0.0:
#                         principal_amt = reducing_val[installment_no - 1]['principal_comp']
#                     if loan.int_payable and interest_rate > 0.0:
#                         interest_amt = reducing_val[installment_no - 1]['interest_comp']
#                     total = principal_amt + interest_amt
#                 installment_obj.create({
#                     'install_no':installment_no + 1,
#                     'date_from':date_from.strftime('%Y-%m-%d'),
#                     'date_to':date_to.strftime('%Y-%m-%d'),
#                     'principal_amt':principal_amt,
#                     'interest_amt':interest_amt,
#                     'total':total,
#                     'loan_id':loan.id
#                 })
# #                date_from = date_from
#                 date_from = date_to
# #                date_to = date_from + relativedelta(months=1)
#                 date_from, date_to = self._get_new_installment_dates(loan, date_from)
#                 install_no += 1
#         return term_change_history_vals
    def update_installments(self, loan, term_change_history_vals):
        print(f'in update_installments = self :{self} - loan:{loan} -term_change_history_vals :{term_change_history_vals} ')
        installment_obj = self.env['partner.loan.installment.details']
        hidden_installment_line_ids = installment_obj.search([('active', '=', False), ('loan_id', '=', loan.id)],
                                                             order='install_no')
        installment_line_ids = loan.installment_lines.filtered(lambda instlmnt: instlmnt.state != 'paid')
        installment_line_ids += hidden_installment_line_ids
        paid_installment_line_ids = loan.installment_lines.filtered(lambda instlmnt: instlmnt.state == 'paid')
        if self.next_instment_date:
            date_disb = self.next_instment_date

            day = date_disb.day
            month = date_disb.month
            year = date_disb.year

            term_change_history_vals.update({
                'old_start_installment_date': installment_line_ids[0].date_from,
                'new_start_installment_date': self.next_instment_date,
            })
        duration = self.duration or loan.duration
        interest_rate = self.interest_rate or loan.int_rate or 0.0
        if self.is_change_duration or self.is_change_int_rate:
            principal_amt, interest_amt, total, reducing_val = self._get_installment_values(loan, duration,
                                                                                            paid_installment_line_ids)
            print(
                f'in update_installments - principal_amt  {principal_amt} - interest_amt:{interest_amt}- total:{total} - reducing_val:{reducing_val}')

        install_no = installment_line_ids[0].install_no
        inst_mnt = installment_line_ids[0]
        reduce_val_inst_no = 0
        # inst_mnt_date = installment_line_ids[0].date_from
        for install_mnt in installment_line_ids:
            if duration < install_no:
                install_mnt.write({
                    'active': False,
                })
                continue
            install_mnt_vals = {}
            if self.next_instment_date:
                #                date_from = datetime(year, month, day)
                #                date_to = date_from + relativedelta(months=1)
                date_from, date_to = self._get_next_installment_dates(loan, year, month, day)
                install_mnt_vals.update({
                    'date_from': date_from.strftime('%Y-%m-%d'),
                    'date_to': date_to.strftime('%Y-%m-%d'),
                })
                day, month, year = date_to.day, date_to.month, date_to.year
            if self.is_change_duration or self.is_change_int_rate:
                print(f'in update_installments - in is_change_int_rate ')
                if loan.interest_mode == 'reducing':
                    if interest_rate > 0.0:
                        principal_amt = reducing_val[reduce_val_inst_no]['principal_comp']
                    if loan.int_payable and interest_rate > 0.0:
                        interest_amt = reducing_val[reduce_val_inst_no]['interest_comp']
                    total = principal_amt + interest_amt
                    install_mnt_vals.update({
                        'active': True,
                        'principal_amt': principal_amt,
                        'interest_amt': interest_amt,
                        'total': total,
                        'loan_id': loan.id
                    })
            # if install_mnt_vals:
            if install_mnt_vals and loan.interest_mode != 'fixed_principal':
                print(f'in update_installments - install_mnt_vals:{install_mnt_vals} ')
                install_mnt.write(install_mnt_vals)
            inst_mnt = install_mnt
            install_no += 1
            reduce_val_inst_no += 1

        if duration > inst_mnt.install_no:
            print(f'in case duration > inst_mnt.install_no - durationL:{duration} - inst_mnt.install_no:{inst_mnt.install_no}')
            date_from = inst_mnt.date_to
            #            date_to = inst_mnt.date_to + relativedelta(months=1)
            date_from, date_to = self._get_new_installment_dates(loan, date_from)
            for installment_no in range(inst_mnt.install_no, duration):
                if loan.interest_mode == 'reducing':
                    if interest_rate > 0.0:
                        principal_amt = reducing_val[installment_no - 1]['principal_comp']
                    if loan.int_payable and interest_rate > 0.0:
                        interest_amt = reducing_val[installment_no - 1]['interest_comp']
                    total = principal_amt + interest_amt
                installment_obj.create({
                    'install_no': installment_no + 1,
                    'date_from': date_from.strftime('%Y-%m-%d'),
                    'date_to': date_to.strftime('%Y-%m-%d'),
                    'principal_amt': principal_amt,
                    'interest_amt': interest_amt,
                    'total': total,
                    'loan_id': loan.id
                })
                #                date_from = date_from
                date_from = date_to
                #                date_to = date_from + relativedelta(months=1)
                date_from, date_to = self._get_new_installment_dates(loan, date_from)
                install_no += 1
        return term_change_history_vals

    def action_update_installment(self):
        if not self.is_confirm_change_term:
            raise ValidationError("We can not update terms since you are still not sure !")
        if not (self.next_instment_date or self.duration or self.interest_rate):
            raise ValidationError("You have entered wrong terms options please check.")
        term_change_history_vals = {}
        loan_ids = self.env['partner.loan.details'].browse(self._context.get('active_ids'))
        old_duration = loan_ids.duration
        old_int_rate = loan_ids.int_rate
        loan_vals = {
            'is_loan_term_changed': True,
        }
        if self.duration:
            loan_vals.update({
                'duration': self.duration,
            })
        if self.interest_rate:
            loan_vals.update({
                'int_rate': self.interest_rate,
            })
        if loan_vals:
            loan_ids.write(loan_vals)
        term_change_history_vals = self.update_installments(loan_ids, term_change_history_vals)
        term_change_history_vals = self._prepare_term_change_history_vals(loan_ids, term_change_history_vals)
        if term_change_history_vals:
            term_change_history_vals.update({
                'old_duration': old_duration,
                'old_int_rate': old_int_rate,
            })
            self.env['term.change.history'].create(term_change_history_vals)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
