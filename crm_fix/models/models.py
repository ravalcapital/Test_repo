from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class CrmInherit(models.Model):
    _inherit = 'crm.lead'

    @api.onchange('contract_term')
    def _onchange_contract_term(self):
        print(f'in _onchange_contract_term ')
        for rec in self:
            print(f'rec.contract_term: {rec.contract_term}')


    def action_sale_quotations_new(self):
        mla_obj = self.env['mla.data'].search(
            [('partner_id', '=', self.partner_id.id), ('state', 'in', ('active', 'to_expire'))])
        if not mla_obj and self.contract_term == 'long_term':
            raise ValidationError(_('No Valid MLA, Please Create One First'))

        return super(CrmInherit, self).action_sale_quotations_new()


class CrmCarDetails(models.Model):
    _inherit = 'crm.car.details'

    model_m_ids = fields.Many2many(comodel_name="fleet.vehicle.model", compute='clc_fleet_model_ids')
    product_id = fields.Many2one('product.product', string='Car', required=True,
                                 domain=[('is_vehicle', '=', True),('tracking', '=', 'serial'),
                                         ('split_receipt', '=', True)])

    @api.depends('make_m_id')
    def clc_fleet_model_ids(self):
        for rec in self:
            fleet_model = self.env['fleet.vehicle.model'].search([('brand_id', '=', rec.make_m_id.id)])
            fleet_ids = fleet_model.mapped('id')
            rec.model_m_ids = [(6, 0, fleet_ids)]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('is_vehicle')
    def change_tracking_state(self):
        if self.is_vehicle:
            self.tracking = 'serial'
