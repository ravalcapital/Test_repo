from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    is_rent = fields.Boolean(string="Rent")

    @api.onchange('is_rent')
    def change_type_service(self):
        for this in self:
            if this.is_rent:
                this.detailed_type = 'service'
