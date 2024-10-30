from odoo import models, fields, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order.line'

    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models",
                                 domain="[('brand_id', '=', make_m_id)]")
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers")
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Category")
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year")


class FleetVehicleModelYear(models.Model):
    _name = 'fleet.vehicle.model.year'
    _description = 'Year'
    _rec_name = 'name'
    _order = 'name DESC'

    name = fields.Char(string="Year", required=True)
