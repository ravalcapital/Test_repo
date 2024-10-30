# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    expense_ids = fields.One2many('hr.expense', 'pending_delivery_id', string="Expenses", ondelete='restrict')
    expense_count = fields.Integer(compute="compute_expense_count")

    @api.depends('expense_ids')
    def compute_expense_count(self):
        for rec in self:
            rec.expense_count = len(rec.expense_ids)

    def action_view_expenses(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses'),
            'res_model': 'hr.expense',
            'view_mode': 'tree,form',
            "context": {"pending_delivery_id": self.id},
            'domain': [('id', 'in', self.mapped('expense_ids').ids)],
        }

    def action_create_expenses(self):
        expense_ids = self.mapped('expense_ids')
        list_view = self.env.ref('hr_expense.view_my_expenses_tree')
        form_view = self.env.ref('hr_expense.hr_expense_view_form')
        if len(expense_ids) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Expenses'),
                'res_model': 'hr.expense',
                'view_mode': 'form',
                'views': [[form_view.id, 'form']],
                'context': {'search_default_my_expenses': 1, 'search_default_no_report': 1,
                            "default_pending_delivery_id": self.id},
                'res_id': expense_ids.id,

            }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses'),
            'res_model': 'hr.expense',
            'view_mode': 'list,form',
            'views': [[list_view.id, 'list'], [form_view.id, 'form']],
            'context': {'search_default_my_expenses': 1, 'search_default_no_report': 1,
                        "default_pending_delivery_id": self.id,
                        "default_analytic_account_id": self.analytic_account_id.id,
                        "default_analytic_tag_ids": [(6, 0, self.analytic_tag_ids.ids)]},
            'domain': [('id', 'in', expense_ids.ids)],
        }


class HRExpense(models.Model):
    _inherit = 'hr.expense'

    pending_delivery_id = fields.Many2one('pending.delivery', string="Pending Delivery")
    product_ids_domain = fields.Many2many('product.product', compute='get_product_id_domain')

    @api.depends('pending_delivery_id')
    def get_product_id_domain(self):
        for rec in self:
            if rec.pending_delivery_id:
                domain = [('can_be_expensed', '=', True), ('policy_payment', '=', True), '|',
                          ('company_id', '=', False), ('company_id', '=', self.company_id.id)]
                product_obj = self.env['product.product'].search(domain)
                rec.product_ids_domain = [(6, 0, product_obj.ids)]
            else:
                domain = [('can_be_expensed', '=', True), '|', ('company_id', '=', False),
                          ('company_id', '=', self.company_id.id)]
                product_obj = self.env['product.product'].search(domain)
                rec.product_ids_domain = [(6, 0, product_obj.ids)]

    # @api.onchange('pending_delivery_id')
    # def onchange_pending_delivery_id(self):
    #     for rec in self:
    #         if rec.pending_delivery_id:
    #             domain = [('can_be_expensed', '=', True), ('policy_payment', '=', True), '|',
    #                       ('company_id', '=', False), ('company_id', '=', self.company_id.id)]
    #             return {'domain': {'product_id': domain}}
    #         else:
    #             return {'domain': {'product_id': [('can_be_expensed', '=', True), '|', ('company_id', '=', False),
    #                                               ('company_id', '=', self.company_id.id)]}}


class ProductProduct(models.Model):
    _inherit = 'product.product'

    policy_payment = fields.Boolean(copy=False, string="Pending Delivery Policy Payment")
