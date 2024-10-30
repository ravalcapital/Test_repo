# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PartnerLoanDetails(models.Model):
    _inherit = 'partner.loan.details'

    expense_ids = fields.One2many('hr.expense', 'loan_expense_id', string="Expenses", ondelete='restrict')
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
            "context": {"loan_id": self.id, "edit": 0},
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
                            "default_loan_expense_id": self.id},
                'res_id': expense_ids.id,

            }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses'),
            'res_model': 'hr.expense',
            'view_mode': 'list,form',
            'views': [[list_view.id, 'list'], [form_view.id, 'form']],
            'context': {'search_default_my_expenses': 1, 'search_default_no_report': 1,
                        "default_loan_expense_id": self.id},
            'domain': [('id', 'in', expense_ids.ids)],
        }


class HRExpense(models.Model):
    _inherit = 'hr.expense'

    loan_expense_id = fields.Many2one('partner.loan.details', string="Loan Request")

    @api.depends('pending_delivery_id', 'loan_expense_id')
    def get_product_id_domain(self):
        for rec in self:
            if rec.pending_delivery_id:
                domain = [('can_be_expensed', '=', True), ('policy_payment', '=', True), '|',
                          ('company_id', '=', False), ('company_id', '=', self.company_id.id)]
                product_obj = self.env['product.product'].search(domain)
                rec.product_ids_domain = [(6, 0, product_obj.ids)]
            elif rec.loan_expense_id:
                domain = [('can_be_expensed', '=', True), ('loan_expense', '=', True), '|',
                          ('company_id', '=', False), ('company_id', '=', self.company_id.id)]
                product_obj = self.env['product.product'].search(domain)
                rec.product_ids_domain = [(6, 0, product_obj.ids)]
            else:
                domain = [('can_be_expensed', '=', True), '|', ('company_id', '=', False),
                          ('company_id', '=', self.company_id.id)]
                product_obj = self.env['product.product'].search(domain)
                rec.product_ids_domain = [(6, 0, product_obj.ids)]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    loan_expense = fields.Boolean(copy=False, string="Loan Expenses")
