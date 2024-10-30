from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models")
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers")
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Category")
    is_vehicle = fields.Boolean(string="Is Vehicle", related="product_id.is_vehicle")
    split_receipt = fields.Boolean(string="Pending Delivery", related="product_id.split_receipt")
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year")
    color_id = fields.Many2one("crm.car.color")


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models")
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers")
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Category")
    is_vehicle = fields.Boolean(string="Is Vehicle", related="product_id.is_vehicle")
    split_receipt = fields.Boolean(string="Pending Delivery", related="product_id.split_receipt")
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    pending_delivery_id = fields.Many2one("pending.delivery", string="Pending Delivery")
