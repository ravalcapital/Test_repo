from odoo import models, fields, api, _


class Resbank(models.Model):
    _inherit = 'res.bank'

    iban = fields.Char('IBAN')
    swift_code = fields.Char('Swift Code')
    branch_no = fields.Char('Branch No.')

class Respartnerbank(models.Model):
    _inherit = 'res.partner.bank'

    iban = fields.Char('IBAN')
    swift_code = fields.Char('Swift Code')
    branch_no = fields.Char('Branch No.')
