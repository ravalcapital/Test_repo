# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    bill_count = fields.Integer(string='Bills', compute='_compute_bill_count')
    invoice_ids = fields.One2many('account.move', 'pending_delivery_id', string='Bills', copy=False)

    def _compute_bill_count(self):
        for pending_id in self:
            move_ids = pending_id.env['account.move'].search([('invoice_origin', '=', pending_id.name)])
            if move_ids:
                self.bill_count = len(move_ids)
            else:
                self.bill_count = 0

    def create_bill(self):
        for pending_id in self:
            current_user = self.env.uid
            vendor_journal_id = pending_id.env['ir.config_parameter'].sudo().get_param(
                'stock_move_invoice.vendor_journal_id') or False
            if not vendor_journal_id:
                raise UserError(_("Please configure the journal from the settings."))
            # bill_line_list = []
            # vals = (0, 0, {
            #     'name': pending_id.purchase_line_id.name,
            #     'product_id': pending_id.purchase_line_id.product_id.id,
            #     'price_unit': pending_id.purchase_line_id.product_id.lst_price,
            #     'account_id': pending_id.purchase_line_id.product_id.property_account_income_id.id if pending_id.purchase_line_id.product_id.property_account_income_id
            #     else pending_id.purchase_line_id.product_id.categ_id.property_account_income_categ_id.id,
            #     'tax_ids': [(6, 0, [pending_id.purchase_line_id.taxes_id.ids])],
            #     'quantity': pending_id.purchase_line_id.product_uom_qty,
            # })
            # bill_line_list.append(vals)
            pending_id.env['account.move'].create({'move_type': 'in_invoice',
                                                   'invoice_origin': pending_id.name,
                                                   'invoice_user_id': current_user,
                                                   'narration': pending_id.name,
                                                   'partner_id': pending_id.partner_id.id,
                                                   'currency_id': pending_id.env.user.company_id.currency_id.id,
                                                   'journal_id': int(vendor_journal_id),
                                                   'payment_reference': pending_id.name,
                                                   'pending_delivery_id': pending_id.id,
                                                   'invoice_line_ids': [],
                                                   'is_pending_delivery_bill': True
                                                   })
            invoices = self.invoice_ids

            result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
            # choose the view_mode accordingly
            if len(invoices) > 1:
                result['domain'] = [('id', 'in', invoices.ids)]
            elif len(invoices) == 1:
                res = self.env.ref('account.view_move_form', False)
                form_view = [(res and res.id or False, 'form')]
                if 'views' in result:
                    result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
                else:
                    result['views'] = form_view
                result['res_id'] = invoices.id
            else:
                result = {'type': 'ir.actions.act_window_close'}

            return result

    def action_open_pending_bill(self):
        return {
            'name': 'Bills',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.name)],
            'context': {'create': False},
            'target': 'current'
        }
