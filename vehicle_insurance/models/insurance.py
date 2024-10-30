# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class VehicleInsurance(models.Model):
    _name = "vehicle.insurance"
    _description = "Vehicle Insurance"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection(string="", selection=[('draft', 'Draft'), ('valid', 'Valid'), ('to_renew', 'To Renew'),
                                                   ('expired', 'Expired'), ], default='draft', )
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    model_id = fields.Many2one('fleet.vehicle.model', related='vehicle_id.model_id')
    name = fields.Char(string="Insurance", required=False, )
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle ID", required=False, )
    license_plate = fields.Char(string="Plate no", related='vehicle_id.license_plate', store=True)
    vehicle_name = fields.Char(string="Vehicle name", required=False,  related='vehicle_id.name')
    date_from = fields.Date(string="Insurance Start Date", required=True, track_visibility='onchange' )
    date_to = fields.Date(string="Insurance End date", required=True, track_visibility='onchange' )
    Insurance_line_ids = fields.One2many(comodel_name="vehicle.insurance.line", inverse_name="vehicle_insurance_id",
                                         string="Insurance Line", required=False, track_visibility='onchange' )

    def next_step_action(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'valid'

    def expired_action(self):
        for rec in self:
            rec.state = 'expired'

    def set_draft_action(self):
        for rec in self:
            rec.state = 'draft'

    def vehicle_insurance_cron(self):
        need_renovation_insurances = self.search(
            [('date_to', '<=', fields.Date.today() + relativedelta(months=2)), ('state', '=', 'valid')])
        for insurance in need_renovation_insurances:
            insurance.state = 'to_renew'
        need_validation_insurances = self.search(
            [('date_to', '>', fields.Date.today() + relativedelta(months=2)), ('state', '=', 'to_renew')])
        for insurance in need_validation_insurances:
            insurance.state = 'valid'

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.insurance') or _('New')
        return super(VehicleInsurance, self).create(vals)


class VehicleInsuranceLine(models.Model):
    _name = "vehicle.insurance.line"
    _description = "Vehicle Insurance Line"

    vehicle_insurance_id = fields.Many2one(comodel_name="vehicle.insurance", string="Vehicle Insurance Reference",
                                           required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="User Name", required=False, )
    creation_date = fields.Date(string="Creation date", default=fields.Date.today())
    date_from = fields.Date(string="Date From", required=False, )
    date_to = fields.Date(string="Insurance End Date", required=False, )
    attachment = fields.Binary('Attachment', )
    years_no = fields.Integer(string="No Of years")

