# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        mla_obj = self.env['mla.data'].search(
            [('partner_id', '=', self.partner_id.id), ('state', 'in', ('active', 'to_expire'))])
        if not mla_obj:
            raise ValidationError(_('No Valid MLA, Please Create One First'))
        return result

    def action_quotation_send(self):
        mla_obj = self.env['mla.data'].search(
            [('partner_id', '=', self.partner_id.id), ('state', 'in', ('active', 'to_expire'))])
        if not mla_obj:
            raise ValidationError(_('No Valid MLA, Please Create One First'))
        return super(SaleOrder, self).action_quotation_send()


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_sale_quotations_new(self):
        mla_obj = self.env['mla.data'].search(
            [('partner_id', '=', self.partner_id.id), ('state', 'in', ('active', 'to_expire'))])
        if not mla_obj and self.contract_term == 'long_term':
            raise ValidationError(_('No Valid MLA, Please Create One First'))
        if mla_obj and self.contract_term == 'shor_term':
            raise ValidationError(_('No Valid MLA, Please Create One First'))
        return super(CrmLead, self).action_sale_quotations_new()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    mla_ids = fields.One2many("mla.data", 'partner_id', string="MLA", required=False, )

