from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    is_vo = fields.Boolean(string="", copy=False)
    # vo_ids = fields.One2many('vehicle.order', 'order_id', string="VO", ondelete='restrict')
    vo_ids = fields.One2many('vehicle.order', 'order_id', string="VO")
    vo_count = fields.Integer(compute="compute_vo_count")

    @api.depends('vo_ids')
    def compute_vo_count(self):
        for rec in self:
            rec.vo_count = len(rec.vo_ids)

    def action_view_vo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('VO'),
            'res_model': 'vehicle.order',
            'view_mode': 'tree,form',
            "context": {"order_id": self.id,
                        'default_option_to_puy': self.option_to_puy,
                        'default_contract_term': self.contract_term,
                        'default_millage_calculation': self.millage_calculation,
                        'default_total_pool_millage': self.total_pool_millage},
            'domain': [('id', 'in', self.mapped('vo_ids').ids)],
        }

    def create_vo_button(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        print(employee)
        for line in self.order_line:
            vals = {
                'state': 'draft',
                'make_id': line.make_m_id.id,
                'model_id': line.model_m_id.id,
                'year_id': line.year_id.id,
                'duration': line.duration_in_month,
                'no_Vehicles': line.product_uom_qty,
                'order_id': self.id,
                'customer_id': self.partner_id.id,
                'created_by': employee.id,
                'product_id': line.product_id.id,
                'currency': line.currency_id.id,
                'unit_price': line.price_unit,
                'vat': line.tax_id.id,
                'total_qty': line.price_subtotal,
                'option_to_puy': self.option_to_puy,
                'contract_term': self.contract_term,
                'millage_calculation': self.millage_calculation,
                'total_pool_millage': self.total_pool_millage
            }

            vo = self.env['vehicle.order'].create(vals)
            self.is_vo = True
            print('********', vo, '***********')


class VoTerms(models.Model):
    _name = 'vo.term'
    _rec_name = 'name'

    name = fields.Char(string="Title")
    terms = fields.Text(string="", required=False, )
