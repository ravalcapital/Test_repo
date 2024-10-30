from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        car_identity_id = []
        for order in self:
            for rec in order.order_line:
                car_identity_id.append(rec.car_identity_id.id)
            for pick in order.picking_ids:
                i = -1
                for line in pick.move_ids_without_package:
                    i += 1
                    if car_identity_id:
                        line.write({'car_identity_ids': [(6, 0, [car_identity_id[i]])], })
        return result


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    car_identity_id = fields.Many2one('car.identity', 'Car Identity')
