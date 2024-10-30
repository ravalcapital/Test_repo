import calendar
from dateutil.relativedelta import relativedelta
from math import copysign

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero, float_round


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    value_residual = fields.Monetary(string='Depreciable Value', compute='_compute_value_residual',
                                     inverse='_clc_value_residual')

    used_car = fields.Boolean(string="Used Car", )

    def _get_disposal_moves(self, invoice_line_ids, disposal_date):
        def get_line(asset, amount, account):
            return (0, 0, {
                'name': asset.name,
                'account_id': account.id,
                'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'analytic_account_id': account_analytic_id.id if asset.asset_type == 'sale' else False,
                'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if asset.asset_type == 'sale' else False,
                'currency_id': current_currency.id,
                'amount_currency': -asset.value_residual,
            })

        move_ids = []
        assert len(self) == len(invoice_line_ids)
        for asset, invoice_line_id in zip(self, invoice_line_ids):
            posted_moves = asset.depreciation_move_ids.filtered(lambda x: (
                    not x.reversal_move_id
                    and x.state == 'posted'
            ))
            if posted_moves and disposal_date < max(posted_moves.mapped('date')):
                if invoice_line_id:
                    raise UserError(
                        'There are depreciation posted after the invoice date (%s).\nPlease revert them or change the date of the invoice.' % disposal_date)
                else:
                    raise UserError('There are depreciation posted in the future, please revert them.')
            account_analytic_id = asset.account_analytic_id
            analytic_tag_ids = asset.analytic_tag_ids
            company_currency = asset.company_id.currency_id
            current_currency = asset.currency_id
            prec = company_currency.decimal_places
            unposted_depreciation_move_ids = asset.depreciation_move_ids.filtered(lambda x: x.state == 'draft')

            old_values = {
                'method_number': asset.method_number,
            }

            # Remove all unposted depr. lines
            commands = [(2, line_id.id, False) for line_id in unposted_depreciation_move_ids]

            # Create a new depr. line with the residual amount and post it
            asset_sequence = len(asset.depreciation_move_ids) - len(unposted_depreciation_move_ids) + 1

            initial_amount = asset.original_value
            initial_account = asset.original_move_line_ids.account_id if len(
                asset.original_move_line_ids.account_id) == 1 else asset.account_asset_id
            depreciation_moves = asset.depreciation_move_ids.filtered(
                lambda r: r.state == 'posted' and not (r.reversal_move_id and r.reversal_move_id[0].state == 'posted'))
            depreciated_amount_used_car = (depreciation_moves[:1].asset_depreciated_value + self.salvage_value)
            depreciated_amount_not_used_car = copysign(
                sum(depreciation_moves.mapped('amount_total')) + asset.already_depreciated_amount_import,
                -initial_amount,
            )
            depreciated_amount = - depreciated_amount_used_car if self.used_car else depreciated_amount_not_used_car
            depreciation_account = asset.account_depreciation_id
            invoice_amount = copysign(invoice_line_id.price_subtotal, -initial_amount)
            invoice_account = invoice_line_id.account_id
            difference = -initial_amount - depreciated_amount - invoice_amount
            difference_account = asset.company_id.gain_account_id if difference > 0 else asset.company_id.loss_account_id
            line_datas = [(initial_amount, initial_account), (depreciated_amount, depreciation_account),
                          (invoice_amount, invoice_account), (difference, difference_account)]
            if not invoice_line_id:
                del line_datas[2]
            vals = {
                'asset_id': asset.id,
                'ref': asset.name + ': ' + (_('Disposal') if not invoice_line_id else _('Sale')),
                'asset_remaining_value': 0,
                'asset_depreciated_value': max(asset.depreciation_move_ids.filtered(lambda x: x.state == 'posted'),
                                               key=lambda x: x.date,
                                               default=self.env['account.move']).asset_depreciated_value,
                'date': disposal_date,
                'journal_id': asset.journal_id.id,
                'line_ids': [get_line(asset, amount, account) for amount, account in line_datas if account],
            }
            commands.append((0, 0, vals))
            asset.write({'depreciation_move_ids': commands, 'method_number': asset_sequence})
            tracked_fields = self.env['account.asset'].fields_get(['method_number'])
            changes, tracking_value_ids = asset._mail_track(tracked_fields, old_values)
            if changes:
                asset.message_post(body=_('Asset sold or disposed. Accounting entry awaiting for validation.'),
                                   tracking_value_ids=tracking_value_ids)
            move_ids += self.env['account.move'].search([('asset_id', '=', asset.id), ('state', '=', 'draft')]).ids

        return move_ids

    # def set_to_close(self, invoice_line_id, date=None):
    #     self.ensure_one()
    #     disposal_date = date or fields.Date.today()
    #     if invoice_line_id and self.children_ids.filtered(
    #             lambda a: a.state in ('draft', 'open') or a.value_residual > 0):
    #         raise UserError(
    #             _("You cannot automate the journal entry for an asset that has a running gross increase. Please use 'Dispose' on the increase(s)."))
    #     full_asset = self + self.children_ids
    #     move_ids = full_asset._get_disposal_moves([invoice_line_id] * len(full_asset), disposal_date)
    #     print(move_ids, invoice_line_id.credit)
    #     move = self.env['account.move'].browse(move_ids)
    #     for mv in move:
    #         depreciation_moves = self.depreciation_move_ids.filtered(
    #             lambda r: r.state == 'posted' and not (r.reversal_move_id and r.reversal_move_id[0].state == 'posted'))
    #         print( mv.invoice_line_ids[1].debit, mv.invoice_line_ids[3].debit,depreciation_moves[:1].asset_depreciated_value+self.salvage_value,mv.invoice_line_ids.mapped('debit'),mv.invoice_line_ids.mapped('credit'))
    #         mv_debit = self.original_value - (
    #                     depreciation_moves[:1].asset_depreciated_value + self.salvage_value + mv.invoice_line_ids[
    #                 2].debit)
    #         mv_lin_debit= depreciation_moves[:1].asset_depreciated_value + self.salvage_value
    #         print(mv_debit,mv_lin_debit)
    #         mv.invoice_line_ids[3].update({'debit':self.original_value-(depreciation_moves[:1].asset_depreciated_value+self.salvage_value+mv.invoice_line_ids[2].debit)})
    #         mv.invoice_line_ids[1].update({'debit' : depreciation_moves[:1].asset_depreciated_value+self.salvage_value})
    #         print(depreciation_moves, mv.invoice_line_ids.mapped('debit'),mv.invoice_line_ids.mapped('credit'))
    #
    #         print(mv.invoice_line_ids[1].debit)
    #         stop
    #
    #     full_asset.write({'state': 'close'})
    #     if move_ids:
    #         return self._return_disposal_view(move_ids)

    def _clc_value_residual(self):
        for rec in self:
            if rec.value_residual:
                rec.salvage_value = rec.original_value - rec.value_residual


class AssetSell(models.TransientModel):
    _inherit = 'account.asset.sell'

    def do_action(self):
        self.ensure_one()
        invoice_line = self.env[
            'account.move.line'] if self.action == 'dispose' else self.invoice_line_id or self.invoice_id.invoice_line_ids
        return self.asset_id.set_to_close(invoice_line_id=invoice_line, date=invoice_line.move_id.invoice_date)


class AccountAccount(models.Model):
    _inherit = 'account.account'

    is_expense = fields.Boolean(string="Expense")
