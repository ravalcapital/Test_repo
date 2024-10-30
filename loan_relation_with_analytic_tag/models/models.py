import time

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError, ValidationError


class LoanDetailsInherit(models.Model):
    _inherit = 'partner.loan.details'

    analytic_tags_id = fields.Many2many('account.analytic.tag', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", required=True)

    @api.constrains('analytic_tags_id')
    def change_analytic_tag(self):
        for line in self.installment_lines:
            line.analytic_tags_id = self.analytic_tags_id.ids

    def action_disburse(self):
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for loan in self:

            if loan.loan_type.disburse_method == 'payroll':
                loan.write({'state': 'disburse'})
                return True
            vals = {}
            #             period_id = period_pool.find(loan.date_applied)[0]
            timenow = time.strftime('%Y-%m-%d')
            address_id = loan.partner_id or False
            partner_id = address_id and address_id and address_id.id or False

            if not partner_id:
                raise ValidationError(_('Please configure Home Address On partner.'))

            move = {
                'narration': loan.name,
                'date': loan.date_disb,
                'ref': loan.name,
                'journal_id': loan.journal_id.id,
                #                 'period_id': period_id.id,
            }
            move_inrest = {
                'narration': loan.name,
                'date': loan.date_disb,
                'ref': loan.name,
                'journal_id': loan.journal_id2.id,
                #                 'period_id': period_id.id,
            }
            credit_account_id = loan.journal_id.default_account_id
            if not loan.journal_id:
                raise ValidationError(_('Please configure Disburse Journal.'))
            if not credit_account_id:
                raise ValidationError(
                    _('Please configure Debit/Credit accounts on the Journal %s ') % (loan.journal_id.name))
            credit_account_id = credit_account_id.id
            debit_account_id = loan.partner_loan_account.id or False
            if not debit_account_id:
                raise ValidationError(_('Please configure debit account of partner'))

            debit_line = (0, 0, {
                'name': _('Loan of %s') % (loan.name),
                'date': loan.date_disb,
                'partner_id': partner_id,
                'account_id': debit_account_id,
                'journal_id': loan.journal_id.id,
                #                     'period_id': period_id.id,
                'debit': loan.principal_amount,
                'credit': 0.0,
                'analytic_tag_ids': [(6, 0, loan.analytic_tags_id.ids)] if loan.partner_loan_account.is_expense else False,
                'analytic_account_id': loan.analytic_account_id.id if loan.partner_loan_account.is_expense else False,

            })
            credit_line = (0, 0, {
                'name': _('Loan of %s') % (loan.name),
                'date': loan.date_disb,
                'partner_id': partner_id,
                'account_id': credit_account_id,
                'journal_id': loan.journal_id.id,
                #                     'period_id': period_id.id,
                'debit': 0.0,
                'credit': loan.principal_amount,
                'analytic_tag_ids':  [(6, 0, loan.analytic_tags_id.ids)] if loan.journal_id.default_account_id.is_expense else False,
                'analytic_account_id': loan.analytic_account_id.id if loan.journal_id.default_account_id.is_expense else False,

            })
            if loan.int_rate > 0.0:
                vals = self._interest_journal(loan, move_inrest, vals, partner_id, move_pool)

            move.update({'line_ids': [debit_line, credit_line]})
            move_id = move_pool.create(move)
            date_disb = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
            if not loan.date_disb:
                vals.update(state='disburse', move_id=move_id.id, date_disb=date_disb)
            else:
                vals.update(state='disburse', move_id=move_id.id)
            loan.write(vals)
        #             if loan.journal_id.entry_posted:#todoprobuse
        #             move_id.post()
        return True


class PartnerLoanInstallmentDetails(models.Model):
    _inherit = 'partner.loan.installment.details'

    analytic_tags_id = fields.Many2many('account.analytic.tag', required=True)

    def book_interest_new(self):
        print('login==============')
        move_pool = self.env['account.move']
        for install in self:
            vals = {}
            timenow = time.strftime('%Y-%m-%d')
            address_id = install.partner_id or False
            partner_id = address_id and address_id and address_id.id or False
            analytic_tag = [(6, 0, install.loan_id.analytic_tags_id.ids)]
            analytic_account = install.loan_id.analytic_account_id.id
            if not partner_id:
                raise ValidationError(_('Please configure Home Address On partner.'))

            move = {
                'narration': install.name,
                'date': install.date_from,
                'ref': install.name,
                'journal_id': install.bank_journal_id.id,
            }
            if install.interest_amt > 0.0:
                credit_account_id = install.recievable_account_id
                if not install.bank_journal_id:
                    raise ValidationError(_('Please configure Bank Journal.'))
                if not credit_account_id:
                    raise ValidationError(
                        _('Please configure Debit/Credit accounts on the Journal %s ') % (install.bank_journal_id.name))
                credit_account_id = credit_account_id.id
                debit_account_id = install.bank_account_id.id or False
                if not debit_account_id:
                    raise ValidationError(_('Please configure debit account of partner'))
                print('install.analytic_tags_id.ids', install.loan_id.analytic_tags_id.ids)
                debit_line = (0, 0, {
                    'name': _('Interest of Installment No. %s of %s') % (install.install_no, install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': debit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'debit': install.interest_amt,
                    'analytic_tag_ids': analytic_tag if install.bank_account_id.is_expense else False,
                    'analytic_account_id': analytic_account if install.bank_account_id.is_expense else False,

                    'credit': 0.0,
                })
                credit_line = (0, 0, {
                    'name': _('Interest of Installment No. %s of %s') % (install.install_no, install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': credit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'analytic_tag_ids': analytic_tag if install.recievable_account_id.is_expense else False,
                    'analytic_account_id': analytic_account if install.recievable_account_id.is_expense else False,

                    'debit': 0.0,
                    'credit': install.interest_amt,
                })
                debit_line_vat, credit_line_vat = self._get_tax_lines(install)
                if debit_line_vat and credit_line_vat:
                    move.update({'line_ids': [debit_line, credit_line, debit_line_vat, credit_line_vat]})
                else:
                    move.update({'line_ids': [debit_line, credit_line]})
                # move.update({'line_ids': [debit_line, credit_line]})
                move_id = move_pool.create(move)
                date_from = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
                if not install.date_from:
                    vals.update(int_move_id=move_id.id, date_from=date_from)
                else:
                    vals.update(int_move_id=move_id.id)
                install.write(vals)
        return True

    def action_pay_installment(self):
        move_pool = self.env['account.move']

        for install in self:
            vals = {}
            analytic_tag = [(6, 0, install.loan_id.analytic_tags_id.ids)]
            analytic_account = install.loan_id.analytic_account_id.id

            timenow = time.strftime('%Y-%m-%d')
            address_id = install.partner_id or False
            partner_id = address_id and address_id and address_id.id or False

            if not partner_id:
                raise ValidationError(_('Please configure Home Address On partner.'))

            move = {
                'narration': install.name,
                'date': install.date_from,
                'ref': install.name,
                'journal_id': install.bank_journal_id.id,
            }
            move_principle = {
                'narration': install.name,
                'date': install.date_from,
                'ref': install.name,
                'journal_id': install.bank_journal_id.id,
            }

            if not install.bank_journal_id:
                raise ValidationError(_('Please configure Bank Journal.'))

            if install.interest_amt == 0.0:
                credit_account_id = install.loan_id.partner_loan_account.id or False
                debit_account_id = install.bank_account_id.id or False
                if not credit_account_id:
                    raise ValidationError(_('Please configure Debit/Credit accounts on the Journal %s ') % (
                        install.bank_journal_id.name))
                if not debit_account_id:
                    raise ValidationError(_('Please configure debit account of partner'))

                debit_line = (0, 0, {
                    'name': _('Installment of %s') % (install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': debit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'analytic_tag_ids': analytic_tag if install.bank_account_id.is_expense else False,
                    'analytic_account_id': analytic_account if install.bank_account_id.is_expense else False,
                    'debit': install.total,
                    'credit': 0.0,
                })
                credit_line = (0, 0, {
                    'name': _('Installment of %s') % (install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': credit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'debit': 0.0,
                    'analytic_tag_ids': analytic_tag if install.loan_id.partner_loan_account.is_expense else False,
                    'analytic_account_id': analytic_account if install.loan_id.partner_loan_account.is_expense else False,

                    'credit': install.total,
                })
            if install.interest_amt > 0.0:
                debit_account_id = install.bank_account_id.id or False
                credit_account_id = install.loan_id.partner_loan_account.id or False
                if not credit_account_id:
                    raise ValidationError(_('Please configure Debit/Credit accounts on the Journal %s ') % (
                        install.bank_journal_id.name))
                if not debit_account_id:
                    raise ValidationError(_('Please configure debit account of partner'))

                debit_line = (0, 0, {
                    'name': _('Installment of %s') % (install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': debit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'analytic_tag_ids': analytic_tag if install.bank_account_id.is_expense else False,
                    'analytic_account_id': analytic_account if install.bank_account_id.is_expense else False,
                    'debit': install.total,
                    'credit': 0.0,
                })
                credit_line = (0, 0, {
                    'name': _('Installment of %s') % (install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': credit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'analytic_tag_ids': analytic_tag if install.loan_id.partner_loan_account.is_expense else False,
                    'analytic_account_id': analytic_account if install.loan_id.partner_loan_account.is_expense else False,

                    'debit': 0.0,
                    'credit': install.total,
                })
                total_debit_account_id = install.loan_id.partner_loan_account.id
                total_credit_account_id = install.loan_id.interest_receivable_account_id.id

                total_debit_line = (0, 0, {
                    'name': _('Interest of Installment No. %s of %s') % (install.install_no, install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': total_debit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'debit': install.interest_amt,
                    'analytic_tag_ids': analytic_tag if install.loan_id.partner_loan_account.is_expense else False,
                    'analytic_account_id': analytic_account if install.loan_id.partner_loan_account.is_expense else False,

                    'credit': 0.0,
                })
                total_credit_line = (0, 0, {
                    'name': _('Interest of Installment No. %s of %s') % (install.install_no, install.loan_id.name),
                    'date': install.date_from,
                    'partner_id': partner_id,
                    'account_id': total_credit_account_id,
                    'journal_id': install.bank_journal_id.id,
                    'debit': 0.0,
                    'analytic_tag_ids': analytic_tag if install.loan_id.interest_receivable_account_id.is_expense else False,
                    'analytic_account_id': analytic_account if install.loan_id.interest_receivable_account_id.is_expense else False,

                    'credit': install.interest_amt,
                })
                move_principle.update({'line_ids': [total_debit_line, total_credit_line]})
                total_move_id = move_pool.create(move_principle)
                if not install.date_from:
                    vals.update(move_id=total_move_id.id)
                else:
                    vals.update(move_id=total_move_id.id)

            move.update({'line_ids': [debit_line, credit_line]})
            move_id = move_pool.create(move)
            date_from = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

            if not install.date_from:
                vals.update(state='paid', total_amt_move_id=move_id.id, date_from=date_from)
            else:
                vals.update(state='paid', total_amt_move_id=move_id.id)
            install.write(vals)
        return True

    def book_interest(self):  # todoprobuse
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for installment in self:
            if installment.loan_id.loan_type.payment_method == 'cash':
                if installment.loan_id:
                    if installment.loan_id.state != 'disburse':
                        raise ValidationError(_('Loan is not Disbursed yet !'))
                    if installment.int_move_id:
                        raise ValidationError(_('Book interest entry is already generated !'))
                #             period_id = period_pool.find(installment.date_from)[0]
                timenow = time.strftime('%Y-%m-%d')
                address_id = installment.loan_id.partner_id or False
                partner_id = address_id and address_id.id or False
                analytic_tag = [(6, 0, installment.loan_id.analytic_tags_id.ids)],

                analytic_account = installment.loan_id.analytic_account_id.id

                if not partner_id:
                    raise ValidationError(_('Please configure Home Address for Partner !'))
                print('installment', installment.loan_id.analytic_tags_id.ids)
                move = {
                    'narration': installment.loan_id.name,
                    'date': installment.date_from,
                    'ref': installment.install_no,
                    'journal_id': installment.loan_id.journal_id2.id,
                    #                 'period_id': period_id,
                }
                #                 debit_account_id = installment.loan_id.journal_id2.default_debit_account_id
                #                 if not debit_account_id:
                #                     raise Warning( _('Please configure Debit/Credit accounts on the Journal %s ') % (installment.journal_id.name))
                #                 debit_account_id = debit_account_id.id
                deb_interest_line = (0, 0, {
                    'name': _('Interest of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.partner_loan_account.id,
                    'journal_id': installment.loan_id.journal_id2.id,
                    #                     'period_id': period_id,
                    'debit': installment.interest_amt,
                    'analytic_tag_ids': analytic_tag if installment.loan_id.partner_loan_account.is_expense else False,
                    'analytic_account_id': analytic_account if installment.loan_id.partner_loan_account.is_expense else False,
                    'credit': 0.0
                })

                cred_interest_line = (0, 0, {
                    'name': _('Interest of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.loan_type.loan_interest_account.id,
                    'journal_id': installment.loan_id.journal_id2.id,
                    #                     'period_id': period_id,
                    'credit': installment.interest_amt,
                    'analytic_tag_ids': analytic_tag if installment.loan_id.loan_type.loan_interest_account.is_expense else False,
                    'analytic_account_id': analytic_account if installment.loan_id.loan_type.loan_interest_account.is_expense else False,

                    'debit': 0.0
                })
                move.update({'line_ids': [deb_interest_line, cred_interest_line]})
                inst_move_id = move_pool.create(move)
                installment.write({'int_move_id': inst_move_id.id})
        #             if installment.loan_id.journal_id2.entry_posted:
        #                 inst_move_id.post()
        return True

    def pay_installment(self):  # ok #probusetodo when call from form view of opening balance
        ctx = dict(self._context or {})
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for installment in self:
            if installment.loan_id.state != 'disburse':
                raise ValidationError(_('Loan is not Disbursed yet !'))
            if installment.loan_id.loan_type.payment_method == 'cash':
                #                 period_id = period_pool.find(installment.date_from)[0]
                timenow = time.strftime('%Y-%m-%d')
                address_id = installment.loan_id.partner_id or False
                partner_id = address_id and address_id.id or False

                if not partner_id:
                    raise ValidationError(_('Please configure Home Address for partner !'))

                move = {
                    'narration': installment.loan_id.name,
                    'date': installment.date_from,
                    'ref': installment.install_no,
                    'journal_id': installment.loan_id.journal_id.id,
                    #                     'period_id': period_id,
                }
                if not installment.loan_id.journal_id.default_account_id:
                    raise ValidationError(
                        _('Please configure Debit/Credit accounts on the Journal %s ') % (self.journal_id.name))

                analytic_tag = [(6, 0, installment.loan_id.analytic_tags_id.ids)],
                analytic_account = installment.loan_id.analytic_account_id.id

                debit_line = (0, 0, {
                    'name': _('EMI of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.journal_id.default_account_id.id,
                    'journal_id': installment.loan_id.journal_id.id,
                    #                         'period_id': period_id,
                    'debit': installment.total,
                    'analytic_tag_ids': analytic_tag if installment.loan_id.journal_id.default_account_id.is_expense else False,
                    'analytic_account_id': analytic_account if installment.loan_id.journal_id.default_account_id.is_expense else False,

                    'credit': 0.0,
                })
                credit_line = (0, 0, {
                    'name': _('EMI of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.partner_loan_account.id,
                    'journal_id': installment.loan_id.journal_id.id,
                    #                         'period_id': period_id,
                    'debit': 0.0,
                    'analytic_tag_ids': analytic_tag if installment.loan_id.partner_loan_account.is_expense else False,
                    'analytic_account_id': analytic_account if installment.loan_id.partner_loan_account.is_expense else False,

                    'credit': installment.total,
                })
                move.update({'line_ids': [debit_line, credit_line]})
                move_id = move_pool.create(move)
                installment.write({'state': 'paid', 'move_id': move_id.id})
                #                 if installment.loan_id.journal_id.entry_posted:#todoprobuse
                #                     move_id.post()
                #                 move_id.post()
                installment.loan_id.compute_installments()
                if ctx.get('recompute'):
                    ctx.pop('recompute')
            else:
                installment.write({'state': 'paid'})
        return True
