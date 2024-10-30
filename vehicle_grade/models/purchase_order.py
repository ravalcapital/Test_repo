from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        vehicle_grade = []
        for order in self:
            for rec in order.order_line:
                vehicle_grade.append(rec.vehicle_grade_id.id)
            for pick in order.picking_ids:
                i = -1
                for line in pick.move_ids_without_package:
                    i += 1
                    line.write({'vehicle_grade_id': vehicle_grade[i]})
        return result


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vehicle_grade_id = fields.Many2one('vehicle.grade', string='Vehicle Grade')


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    vehicle_grade_id = fields.Many2one('vehicle.grade', related="purchase_line_id.vehicle_grade_id",
                                       store=True, string='Vehicle Grade')

    def action_create_vehicle(self):
        res = super(PendingDelivery, self).action_create_vehicle()
        if self.vehicle_id:
            self.vehicle_id.vehicle_grade_id = self.vehicle_grade_id.id
        return res
