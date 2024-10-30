# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VehicleOrder(models.Model):
    _inherit = 'vehicle.order'

    product_id = fields.Many2one(comodel_name="product.product")
    manufacturer_id = fields.Many2one(comodel_name="fleet.vehicle.model.brand", string="", required=False)

    def create_rfq_button(self):
        vals = {
            'partner_id': self.customer_id.id,
            'currency_id': self.currency.id or self.env.user.company_id.currency_id.id,
            'date_planned': self.create_date,
            'vo_id': self.id,
            'state': 'draft',
            'mla_id': self.mla_id.id,
            'order_line': [(0, 0, {

                'product_id': self.product_id.id,
                'model_m_id': self.model_id.id,
                'make_m_id': self.make_id.id,
                'year_id': self.year_id.id,
                'product_qty': self.no_Vehicles,
                'price_unit': self.unit_price,
            })]

        }
        self.env['purchase.order'].create(vals)
