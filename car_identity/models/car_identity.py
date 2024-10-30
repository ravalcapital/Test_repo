# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CarIdentity(models.Model):
    _name = 'car.identity'
    _description = 'Car Identity'

    name = fields.Char(string="Name", required=True)

class ChangeCarIdentity(models.Model):
    _name = 'change.car.identity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Change Car Identity'
    _order = 'created_on desc'

    name = fields.Char(string="Sequence", required=True,
                       default="New", copy=False,
                       tracking=True, readonly=1)
    # partner_id = fields.Many2one('res.partner', 'Customer', tracking=True,required=True, domain=[('company_type', '=', 'company')])
    active = fields.Boolean(default=True, tracking=True)
    created_on = fields.Datetime(default=fields.Date.context_today, string="Created On")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')], string='Status',
        copy=False, default='draft', required=True, tracking=True)

    user_id = fields.Many2one('res.users', string="Created By",
                              default=lambda self: self.env.user, tracking=True)
    approved_by_id = fields.Many2one('res.users', string="Approved By",tracking=True)
    approved_on = fields.Datetime(string="Approved on")

    car_identity_line_ids = fields.One2many('change.car.identity.line', 'car_identity_id', string="Lines")
    description = fields.Html("Description")

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('change.car.identity') or '/'
        return super(ChangeCarIdentity, self).create(vals)

    def send_action(self):
        for rec in self:
            rec.state = 'in_progress'

    def approve_action(self):
        for rec in self:
            rec.state = 'approved'
            rec.approved_by_id = self.env.user.id
            rec.approved_on = fields.Datetime.now()
            for line in rec.car_identity_line_ids:
                line.lot_id.car_identity_id = line.new_car_identity_id.id
                if line.lot_id.vehicle_id:
                    line.lot_id.vehicle_id.car_identity_id = line.new_car_identity_id.id

    def cancel_action(self):
        for rec in self:
            rec.state = 'cancelled'

    def set_to_draft_action(self):
        for rec in self:
            rec.state = 'draft'


class ChangeCarIdentityLine(models.Model):
    _name = 'change.car.identity.line'
    _description = 'Car Identity Line'
    _order = 'date desc'

    name = fields.Char(string="Description", required=True, copy=False)
    lot_id = fields.Many2one('stock.production.lot', string="Plate Number")
    date = fields.Date(default=fields.Date.context_today, string="Date")
    car_identity_id = fields.Many2one('change.car.identity', 'Car Identity')
    current_car_identity_id = fields.Many2one('car.identity', string='Current Identity')
    new_car_identity_id = fields.Many2one('car.identity', 'New Identity')

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        for rec in self:
            if rec.lot_id:
                rec.name = rec.lot_id.name
                rec.current_car_identity_id = rec.lot_id.car_identity_id.id
