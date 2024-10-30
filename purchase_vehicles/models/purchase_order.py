from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    pending_delivery_ids = fields.One2many('pending.delivery', 'purchase_id', string="Pending Delivery")
    pending_delivery_count = fields.Integer(compute="compute_pending_delivery_count")

    @api.depends('pending_delivery_ids')
    def compute_pending_delivery_count(self):
        for rec in self:
            rec.pending_delivery_count = len(rec.pending_delivery_ids.ids)

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        model_m_id = []
        make_m_id = []
        category_m_id = []
        year_id = []
        color_id = []
        for order in self:
            for rec in order.order_line:
                model_m_id.append(rec.model_m_id.id)
                make_m_id.append(rec.make_m_id.id)
                category_m_id.append(rec.category_m_id.id)
                year_id.append(rec.year_id.id)
                color_id.append(rec.color_id.id)
                if rec.split_receipt and rec.product_id.tracking == 'serial':
                    x = 1
                    while (x < rec.product_qty + 1):
                        x += 1
                        self.env['pending.delivery'].create({
                            'purchase_id': order.id,
                            'purchase_line_id': rec.id,
                            'model_m_id': rec.model_m_id.id,
                            'company_id': rec.company_id.id,
                            'color_id': rec.color_id.id})

            for pick in order.picking_ids:
                i = -1
                for line in pick.move_ids_without_package:
                    i += 1
                    line.write({'model_m_id': model_m_id[i],
                                'make_m_id': make_m_id[i],
                                'category_m_id': category_m_id[i],
                                'year_id': year_id[i],
                                'color_id': color_id[i],
                                })

        return result

    def action_view_pending_delivery(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pending Delivery'),
            'res_model': 'pending.delivery',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.mapped('pending_delivery_ids').ids)],
        }


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_vehicle = fields.Boolean(string="Is Vehicle", related="product_id.is_vehicle")
    split_receipt = fields.Boolean(string="Pending Delivery", related="product_id.split_receipt")


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle ID")

