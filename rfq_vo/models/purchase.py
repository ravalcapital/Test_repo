from odoo import models, fields, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    vo_id = fields.Many2one(comodel_name="vehicle.order", string="", required=False, )
    mla_id = fields.Many2one(comodel_name="mla.data", string="", required=False, )
