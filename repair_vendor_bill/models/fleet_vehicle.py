# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    repairs_ids = fields.One2many('repair.order', 'vehicle_id', string="Repair Orders", ondelete='restrict')
    repairs_count = fields.Integer(compute="compute_repairs_count")
    driver_chauffeur_id = fields.Many2one('hr.employee', string="Driver Chauffeur")

    def _get_driver_chauffeur_history_data(self, vals):
        self.ensure_one()
        return {
            'vehicle_id': self.id,
            'driver_chauffeur_id': vals['driver_chauffeur_id'],
            'date_start': fields.Date.today(),
        }

    def create_driver_chauffeur_history(self, vals):
        for vehicle in self:
            self.env['fleet.vehicle.chauffeur.log'].create(
                vehicle._get_driver_chauffeur_history_data(vals),
            )

    @api.model
    def create(self, vals):
        res = super(FleetVehicle, self).create(vals)
        if 'driver_chauffeur_id' in vals and vals['driver_chauffeur_id']:
            res.create_driver_chauffeur_history(vals)
        return res

    def write(self, vals):
        if 'driver_chauffeur_id' in vals and vals['driver_chauffeur_id']:
            driver_chauffeur_id = vals['driver_chauffeur_id']
            for vehicle in self.filtered(lambda v: v.driver_chauffeur_id.id != driver_chauffeur_id):
                vehicle.create_driver_chauffeur_history(vals)
                if vehicle.driver_chauffeur_id:
                    vehicle.activity_schedule(
                        'mail.mail_activity_data_todo',
                        user_id=vehicle.manager_id.id or self.env.user.id,
                        note=_('Specify the End date of %s') % vehicle.driver_chauffeur_id.name)

        res = super(FleetVehicle, self).write(vals)
        return res

    @api.depends('repairs_ids')
    def compute_repairs_count(self):
        for rec in self:
            rec.repairs_count = len(rec.repairs_ids)

    def action_view_repairs(self):
        print(f'in action_view_repairs fleet vehicle = :{self} - default_plate_lot_id :{self.lot_id.id} - default_vo_id :{self.vo_id.id} - default_mla_id :{self.mla_id.id} - default_partner_id:{self.customer_id.id}')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Repair Order'),
            'res_model': 'repair.order',
            'view_mode': 'tree,form',
            "context": {
                        "default_plate_lot_id": self.lot_id.id,
                        "default_vo_id": self.vo_id.id,
                        "default_mla_id": self.mla_id.id,
                        "default_partner_id": self.customer_id.id,
                        "default_mobile_number": self.customer_id.mobile,
                        "create": True,
                        'edit': False,
                        'delete': False,
                        'duplicate': False},
            'domain': [('id', 'in', self.mapped('repairs_ids').ids)],
        }

    vo_ids = fields.Many2many('vehicle.order', 'vo_col1_id', 'vo_col2_id', 'vo_rel_id', string="Vehicle Orders",
                              compute="compute_vo_ids")
    vo_count = fields.Integer(compute="compute_vo_count")
    vo_id = fields.Many2one("vehicle.order", string='Current VO')
    mla_id = fields.Many2one(comodel_name="mla.data", string="MLA")
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    @api.depends('vo_id')
    @api.onchange('vo_id')
    def _onchange_vo_id(self):
        if self.vo_id:
            self.mla_id = self.vo_id.mla_id.id
            self.customer_id = self.vo_id.customer_id.id


    @api.depends('vo_ids')
    def compute_vo_count(self):
        for rec in self:
            rec.vo_count = len(rec.vo_ids)

    def compute_vo_ids(self):
        for rec in self:
            vehicle_obj = self.env['vehicle.car.details'].search([('fleet_licence_plate_id', '=', rec.id)])
            vehicle_list = []
            vo_runing = False
            for veh in vehicle_obj:
                if veh.vehicle_order_id.state in ['inprogress','confirmed']:
                   vo_runing = veh.vehicle_order_id.id
                vehicle_list.append(veh.vehicle_order_id.id)
            rec.vo_ids = [(6, 0, vehicle_list)]
            if not rec.vo_id:
                rec.vo_id = vo_runing
                # rec.mla_id = rec.vo_id.mla_id.id
                # rec.customer_id = rec.vo_id.customer_id.id

    def action_view_vo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle Orders'),
            'res_model': 'vehicle.order',
            'view_mode': 'tree,form',
            "context": {"create": False, 'edit': False, 'delete': False, 'duplicate': False},
            'domain': [('id', 'in', self.mapped('vo_ids').ids)],
        }

    log_drivers_chauffeur_ids = fields.One2many('fleet.vehicle.chauffeur.log', 'vehicle_id', string='Driver chauffeur')

    log_drivers_chauffeur_count = fields.Integer(compute="compute_log_drivers_chauffeur_count")

    @api.depends('log_drivers_chauffeur_ids')
    def compute_log_drivers_chauffeur_count(self):
        for rec in self:
            rec.log_drivers_chauffeur_count = len(rec.log_drivers_chauffeur_ids)


    def action_view_log_drivers_chauffeur(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Driver chauffeur'),
            'res_model': 'fleet.vehicle.chauffeur.log',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.mapped('log_drivers_chauffeur_ids').ids)],
            'context': {'default_driver_id': self.driver_id.id, 'default_vehicle_id': self.id}
        }

    # @api.model
    # def crone_car_maintenance_plan_notify(self):
    #     maintenance_plan_obj = self.env['maintenance.schedule.plan'].search([('done', '=', 'no')])
    #     for rec in maintenance_plan_obj:
    #         if rec.notify_sent != True and rec.vehicle_id:
    #             odometer_km = rec.vehicle_id.odometer + 1000
    #             if rec.km_maintenance == odometer_km :
    #                 users = self.env['res.users'].search([])
    #                 for user in users:
    #                     today = fields.Date.today()
    #                     if user.has_group('car_maintenance_reminder.maintenance_schedule_group_user') or user.has_group(
    #                         'car_maintenance_reminder.maintenance_schedule_group_manager'):
    #                         rec.vehicle_id.activity_schedule(
    #                             'repair_vendor_bill.schedule_activity_car_maintenance_plan_notify', today,
    #                             user_id=user.id,
    #                             summary=self.env.user.name + ' ' + 'This Vehicle' + ' ' + rec.vehicle_id.name + ' ' + 'need to be repaired based on maintenance plan'+ ' ' + rec.name)
    #                 rec.notify_sent = True

    @api.model
    def crone_car_maintenance_plan_notify(self):
        maintenance_plan_obj = self.env['maintenance.schedule.plan'].search([('done', '=', 'no')])
        for rec in maintenance_plan_obj:
            if rec.notify_sent != True and rec.vehicle_id:
                odometer_km = rec.vehicle_id.odometer + 1000
                if rec.km_maintenance == odometer_km :
                    # users = self.env['res.users'].search([])
                    repair_car_notified_users = self.env['repair.car.notified.users'].search([], limit=1)
                    for user in repair_car_notified_users.car_notified_users:
                        today = fields.Date.today()
                        # if user.has_group('car_maintenance_reminder.maintenance_schedule_group_user') or user.has_group(
                        #     'car_maintenance_reminder.maintenance_schedule_group_manager'):
                        rec.vehicle_id.activity_schedule(
                            'repair_vendor_bill.schedule_activity_car_maintenance_plan_notify', today,
                            user_id=user.id,
                            summary=self.env.user.name + ' ' + 'This Vehicle' + ' ' + rec.vehicle_id.name + ' ' + 'need to be repaired based on maintenance plan'+ ' ' + rec.name)
                    rec.notify_sent = True



class FleetVehicleChauffeurLog(models.Model):
    _name = "fleet.vehicle.chauffeur.log"
    _description = "Drivers Chauffeur on a vehicle"
    _order = "create_date desc, date_start desc"

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    driver_chauffeur_id = fields.Many2one('hr.employee', string="Driver Chauffeur", required=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")

class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'
    change_tire_every = fields.Float("Change Tire Every", copy=False)
