from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    serial_damage_id = fields.Many2one(comodel_name="damage.vehicle", string="Serial Damage Vehicle", required=False, )