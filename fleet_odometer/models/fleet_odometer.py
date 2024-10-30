# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FleetCarsOdometer(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'fleet.cars.odometer'
    _description = 'Odometer Request for a vehicle'
    _order = 'created_on desc'

    name = fields.Char(string="Sequence", required=True,
                       default="New", copy=False,
                       tracking=True, readonly=1)
    active = fields.Boolean(default=True, tracking=True)
    created_on = fields.Datetime(default=fields.Date.context_today, string="Created On")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')], string='Status',
        copy=False, default='draft', required=True, tracking=True)

    user_id = fields.Many2one('res.users', string="Created By",
                              default=lambda self: self.env.user, tracking=True)
    odometer_line_ids = fields.One2many('fleet.cars.odometer.line', 'odometer_id', string="Cars Odometer")
    odometer_ids = fields.Many2many('fleet.vehicle.odometer', string="Odometers")
    vo_ids = fields.Many2many("vehicle.order", 'car_odometer_col1', 'car_odometer_col2', 'car_odometer_rel',
                              string="VO", domain="[('state', 'in', ['inprogress','draft','confirmed'])]", copy=False)
    vehicle_ids = fields.Many2many('fleet.vehicle', string='Vehicle', copy=False)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.cars.odometer') or '/'
        return super(FleetCarsOdometer, self).create(vals)

    def confirm_action(self):
        for rec in self:
            odometer_list = []
            for line in rec.odometer_line_ids:
                odometer_obj = self.env['fleet.vehicle.odometer'].create({
                    'date': line.date,
                    'value': line.value,
                    'vo_id': line.vo_id.id,
                    'vehicle_id': line.vehicle_id.id,
                })
                vehicle_obj = self.env['fleet.vehicle'].browse(line.vehicle_id.id)
                if vehicle_obj:
                    vehicle_obj.write({
                        'driver_id':line.driver_id.id,
                        'driver_chauffeur_id':line.employee_id.id,
                    })
                line.odometer_vehicle_id = odometer_obj.id
                odometer_list.append(odometer_obj.id)
            rec.odometer_ids = [(6, 0, odometer_list)]
            rec.state = 'done'

    # def get_all_vehicles(self):
    #     for rec in self:
    #         vehicle_list = []
    #         for line in rec.vo_ids:
    #             for vehicle in line.vehicle_car_ids:
    #                 if vehicle.fleet_licence_plate_id:
    #                     vehicle_list.append(vehicle.fleet_licence_plate_id.id)
    #         rec.vehicle_ids = [(6, 0, vehicle_list)]
    #         for veh in rec.vehicle_ids:
    #             self.env['fleet.cars.odometer.line'].create({'odometer_id': self.id,
    #                                                          'name': veh.display_name,
    #                                                          'vehicle_id': veh.id,
    #                                                          'vo_id': veh.vo_id.id,
    #                                                          'value': veh.odometer,
    #                                                          'driver_id': veh.driver_id.id,
    #                                                          'employee_id': veh.driver_chauffeur_id.id,
    #                                                          })

    def get_all_vehicles(self):
        for rec in self:
            vehicle_list = []
            # rec.vehicle_ids = [(5,0,0)]
            # rec.odometer_line_ids = [(5,0,0)]
            for line in rec.vo_ids:
                for vehicle in line.vehicle_car_ids:
                    if vehicle.fleet_licence_plate_id:
                        # vehicle_list.append(vehicle.fleet_licence_plate_id.id)
                        rec.vehicle_ids = [(4,vehicle.fleet_licence_plate_id.id)]
                        vals = {
                                'odometer_id': self.id,
                                'name': vehicle.fleet_licence_plate_id.name,
                                'vehicle_id': vehicle.fleet_licence_plate_id.id,
                                # 'vo_id': vehicle.fleet_licence_plate_id.vo_id.id,
                                'vo_id': line.id,
                                'value': vehicle.fleet_licence_plate_id.odometer,
                                'driver_id': vehicle.fleet_licence_plate_id.driver_id.id,
                                'employee_id': vehicle.fleet_licence_plate_id.driver_chauffeur_id.id,
                              }
                        fleet_odometer_line = self.env['fleet.cars.odometer.line'].create(vals)

class FleetCarsOdometerLine(models.Model):
    _name = 'fleet.cars.odometer.line'
    _description = 'Odometer Line Request for a vehicle'
    _order = 'date desc'

    name = fields.Char(string="Description", copy=False)
    date = fields.Datetime(default=fields.Datetime.now, string="Date")
    value = fields.Float('Odometer Value', group_operator="max")
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True)
    vehicle_driver_id = fields.Many2one(related="vehicle_id.driver_id", string="Driver", readonly=False)
    driver_id = fields.Many2one('res.partner', 'Driver', tracking=True, help='Driver address of the vehicle',
                                copy=False)
    employee_id = fields.Many2one("hr.employee", string='Driver Chauffeur', tracking=True,
                                  help='Driver address of the vehicle', copy=False)
    @api.depends('vehicle_id')
    def get_vehicle_vo(self):
        for rec in self:
            if rec.vehicle_id:
                if rec.vehicle_id.vo_id:
                    rec.vo_id = rec.vehicle_id.vo_id.id
                else:
                    rec.vo_id = False
            else:
                rec.vo_id = False

    # vo_id = fields.Many2one("vehicle.order", string="Current VO",compute='get_vehicle_vo')
    # vo_id = fields.Many2one(related="vehicle_id.vo_id", string="Current VO")
    vo_id = fields.Many2one("vehicle.order", string="Current VO")
    odometer_id = fields.Many2one("fleet.cars.odometer", string="Odometer")
    odometer_vehicle_id = fields.Many2one('fleet.vehicle.odometer', string="Odometer")

    # @api.constrains('date')
    # def _check_date(self):
    #     for rec in self:
    #         odometer_obj = self.search([('vehicle_id', '=', rec.vehicle_id.id), ('date', '>', rec.date)])
    #         if odometer_obj:
    #             raise ValidationError("Car Odometer date overlap")

    @api.onchange('vehicle_id')
    def onchange_vehicle_id_driver(self):
        for rec in self:
            if rec.vehicle_id:
                rec.driver_id = rec.vehicle_id.driver_id.id
                rec.employee_id = rec.vehicle_id.driver_chauffeur_id.id
            else:
                rec.driver_id = False
                rec.employee_id = False
