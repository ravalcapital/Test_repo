# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    vo_id = fields.Many2one(comodel_name="vehicle.order", string="", required=False, )
    mla_id = fields.Many2one(comodel_name="mla.data", string="", required=False, )
    vo_line_id = fields.Many2one(comodel_name="vo.account.payment.line", string="", required=False, )

    def action_post(self):
        res = super(AccountPayment, self).action_post()

        if self.state== 'posted':

            vo_payment = self.env['vo.account.payment.line'].search([('id', '=', self.vo_line_id.id)], limit=1)
            if vo_payment:
                vo_payment.payment_reference = self.name

        return res
