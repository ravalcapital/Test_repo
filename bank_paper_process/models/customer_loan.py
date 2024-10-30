from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LoanModel(models.Model):
    _inherit = 'partner.loan.details'

    bank_paper_ids = fields.One2many('bank.paper', 'loan_id')

    def bank_paper_action(self):
        if not self.bank_paper_ids:
            raise UserError(_('There are no bank paper for this pending delivery.'))
        action = {
            'name': 'Bank Papers',
            'type': 'ir.actions.act_window',
            'res_model': 'bank.paper',
        }
        if len(self.bank_paper_ids) == 1:
            action.update(res_id=self.bank_paper_ids.id, view_mode='form')
        else:
            action.update(domain="[('loan_id', 'in', %s)]" % self.ids, view_mode='tree,form')

        return action
