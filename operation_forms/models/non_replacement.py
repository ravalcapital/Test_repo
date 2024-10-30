from odoo import api, fields, models, _


class NonReplacement(models.Model):
    _name = "non_replacement.model"
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    phone = fields.Char(related='user_name.phone')
    tools_out = fields.Boolean(string="Tools")
    tools_in = fields.Boolean(string="Tools")
    triangle_out = fields.Boolean(string="Triangle")
    triangle_in = fields.Boolean(string="Triangle")
    ashtray_out = fields.Boolean(string="Ashtray")
    ashtray_in = fields.Boolean(string="Ashtray")
    antenna_out = fields.Boolean(string="Antenna")
    antenna_in = fields.Boolean(string="Antenna")
    cassette_out = fields.Boolean(string="Cassette")
    cassette_in = fields.Boolean(string="Cassette")
    ac_port_out = fields.Boolean(string="Ac pots ")
    ac_port_in = fields.Boolean(string="Ac pots ")
    seat_febric_out = fields.Boolean(string="Seat Febric")
    seat_febric_in = fields.Boolean(string="Seat Febric")
    spare_out = fields.Boolean(string="Spare wheel")
    spare_in = fields.Boolean(string="Spare wheel")
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="non_replacement_id", string="", required=False, )


    manual_key_in = fields.Boolean(string="Manual Key")
    manual_key_out = fields.Boolean(string="Manual Key")


    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('non_replacement.model') or _('New')
        return super(NonReplacement, self).create(vals_list)
