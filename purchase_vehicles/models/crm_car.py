from odoo import api, fields, models


class CrmCarColor(models.Model):
    _name = 'crm.car.color'
    _description = 'Car Colors'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color", copy=False)
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.company, readonly=True)