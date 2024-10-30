# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DamageVehicle(models.Model):
    _name = 'damage.vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Damage Vehicle'
    _order = 'created_on desc'

    @api.depends('damage_vehicle_line_ids','damage_vehicle_line_ids.amount')
    def calc_damage_total_cost(self):
        print(f'in cal_damage_total_cost')
        total_cost = 0.0
        for rec in self:
            # for line in rec.damage_vehicle_line_ids:
            #     total_cost += line.amount
            # rec.total_cost = total_cost
            rec.total_cost = sum([line.amount for line in rec.damage_vehicle_line_ids])



    name = fields.Char(string="Sequence", required=True,
                       default="New", copy=False,
                       tracking=True, readonly=1)
    partner_id = fields.Many2one('res.partner', 'Customer', tracking=True,required=True, domain=[('company_type', '=', 'company')])
    active = fields.Boolean(default=True, tracking=True)
    created_on = fields.Datetime(default=fields.Date.context_today, string="Date Created")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')], string='Status',
        copy=False, default='draft', required=True, tracking=True)

    user_id = fields.Many2one('res.users', string="Created By",
                              default=lambda self: self.env.user, tracking=True)
    total_cost = fields.Float('Total Cost',compute='calc_damage_total_cost',store=True,readonly=True)
    type = fields.Selection([
        ('partial_damage', 'Partial Damage'),
        ('total_loss', 'Total Loss')], string='Damage Type',
        required=True, tracking=True)
    insurance_company_id = fields.Many2one('res.partner', 'Insurance Company', tracking=True)
    damage_vehicle_line_ids = fields.One2many('damage.vehicle.line', 'damage_vehicle_id', string="Lines")
    description = fields.Html("Description")
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('damage.vehicle') or '/'
        return super(DamageVehicle, self).create(vals)

    def confirm_action(self):
        for rec in self:
            rec.state = 'done'


class DamageVehicleLine(models.Model):
    _name = 'damage.vehicle.line'
    _description = 'Damage Vehicle Line'
    _order = 'date desc'

    name = fields.Char(string="Description", required=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product', required=True, domain=[('type', '=', 'service'),('is_damage', '=', True)])
    date = fields.Date(default=fields.Date.context_today, string="Date")
    licence_plate = fields.Many2one(comodel_name="stock.production.lot", string="License Plate", required=False, )

    mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", required=False, )
    # license_plate = fields.Char(string="License Plate", related='vehicle_id.license_plate', store=True)
    vo_id = fields.Many2one("vehicle.order", string="Current VO")
    amount = fields.Float('Amount')
    damage_vehicle_id = fields.Many2one('damage.vehicle', 'Damage Vehicle')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.name = rec.product_id.name
