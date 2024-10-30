# -*- coding: utf-8 -*-

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    product_id = fields.Many2one('product.product', 'Product')
    purchase_id = fields.Many2one('purchase.order', string='PO', store=True,
                                  related="purchase_line_id.order_id")
    purchase_line_id = fields.Many2one('purchase.order.line', string='PO Line')
    receive_ids = fields.Many2many('stock.picking', string='Receive ID')
    pending_delivery_id = fields.Many2one('pending.delivery', string='Pending Delivery')
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year")
    lot_id = fields.Many2one('stock.production.lot', string="Lot/Serial")
    location_id = fields.Many2one('stock.location', readonly=False,string="Location",
                         )
    no_of_keys = fields.Integer()

    @api.depends('lot_id', 'lot_id.quant_ids')
    def get_lot_locations(self):
        for rec in self:
            if rec.lot_id:
                stock_quant_obj = self.env['stock.quant'].search(
                    [('lot_id', '=', rec.lot_id.id)], order='id desc', limit=1)
                rec.location_id = stock_quant_obj.location_id.id
            else:
                rec.location_id = False

