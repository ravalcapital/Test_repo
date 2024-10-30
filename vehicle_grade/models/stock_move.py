from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    vehicle_grade_id = fields.Many2one('vehicle.grade', string='Vehicle Grade')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    vehicle_grade_id = fields.Many2one('vehicle.grade', string='Vehicle Grade')
