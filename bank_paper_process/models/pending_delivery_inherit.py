from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    bank_paper_id = fields.Many2one('bank.paper', compute='get_bank_paper', store=True)
    bank_paper_ids = fields.One2many('bank.paper', 'pending_delivery_id', string="Bank Papers")
    bank_paper_created = fields.Boolean(copy=False)
    bank_paper_count = fields.Integer(compute="compute_bank_paper_count")

    @api.depends('bank_paper_ids')
    def compute_bank_paper_count(self):
        for rec in self:
            rec.bank_paper_count = len(rec.bank_paper_ids.ids)

    @api.depends('purchase_id')
    def get_bank_paper(self):
        for rec in self:
            bank_paper = self.env['bank.paper'].search([('vendor_po_id', '=', rec.purchase_id.id)], limit=1)
            # rec.bank_paper_id = bank_paper

    def bank_paper_action(self):
        if not self.bank_paper_id:
            raise UserError(_('There are no bank paper for this pending delivery.'))
        return {
            'name': 'Bank Papers',
            'type': 'ir.actions.act_window',
            'res_model': 'bank.paper',
            'view_mode': 'tree,form',
            # 'res_id': self.bank_paper_id.id,
            'domain': [('id', 'in', self.mapped('bank_paper_ids').ids)],
            'context': {"default_pending_delivery_id": self.id,
                        'default_pending_delivery_lines2': [(4, self.id)],
                        "default_bank_id": self.bank_id.id,
                        "default_bank_account_id": self.bank_account_id.id},

        }

    @api.model
    def create_bank_paper(self):
        all_banks = []
        all_banks_account = []
        all_pending_delivery = []
        for rec in self:
            if rec.bank_paper_created is not True:
                all_banks.append(rec.bank_id.id)
                all_banks_account.append(rec.bank_account_id.id)
                all_pending_delivery.append(rec.id)
        if all_banks and all_banks_account:
            if len(set(all_banks)) == 1 and len(set(all_banks_account)) == 1:
                bank_paper = self.env['bank.paper'].create({
                    'bank_id': all_banks[0],
                    'bank_account_id': all_banks_account[0],
                    'pending_delivery_lines2':[(4, self.id)],
                    'pending_delivery_id':self.id,
                })
                for rec in self:
                    if rec.bank_paper_created is not True:
                        rec.bank_paper_id = bank_paper.id
                        rec.bank_paper_created = True
            else:
                raise ValidationError(_('Please check all Bank Names and Bank Accounts of selected lines.'))
        else:
            raise ValidationError(_('Please check selected lines.'))

    # @api.constrains('bank_id', 'bank_account_id', 'state')
    # def constrain_accounts_paper_created(self):
    #     if self.state == 'bank_papers' and self.bank_id and self.bank_account_id and not self.bank_paper_created:
    #         bank_paper = self.env['bank.paper'].create({
    #             'bank_id': self.bank_id.id,
    #             'bank_account_id': self.bank_account_id.id,
    #             'pending_delivery_lines2': [(4, self.id)],
    #             'pending_delivery_id': self.id,
    #         })
    #         self.bank_paper_id = bank_paper.id
    #         self.bank_paper_created = True

