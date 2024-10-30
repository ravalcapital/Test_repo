# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaintenanceSchedule(models.Model):
    _name = 'maintenance.schedule'
    _description = 'Maintenance Schedule'

    name = fields.Char(string="Sequence", required=True,
                       default="New", copy=False,
                       tracking=True, readonly=1)

    km_maintenance = fields.Float('KM To Maintenance')
    model_id = fields.Many2one('fleet.vehicle.model', 'Models', required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.schedule') or '/'
        return super(MaintenanceSchedule, self).create(vals)

    @api.constrains('km_maintenance')
    def _check_km_maintenance(self):
        for rec in self:
            maintenance_obj = self.search(
                [('km_maintenance', '>', rec.km_maintenance), ('id', '<', rec.id), ('model_id', '=', rec.model_id.id)])
            if maintenance_obj:
                raise ValidationError("The next line should always be greater than previous line")


class MaintenanceSchedulePlan(models.Model):
    _name = 'maintenance.schedule.plan'
    _description = 'Maintenance Schedule Plan'
    _rec_name = "km_maintenance"

    name = fields.Char(string="Sequence", required=True,
                       default="New", copy=False,
                       tracking=True, readonly=1)

    km_maintenance = fields.Float('KM To Maintenance')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True)
    model_id = fields.Many2one('fleet.vehicle.model', 'Models', required=True)
    maintenance_schedule_id = fields.Many2one('maintenance.schedule')
    repair_id = fields.Many2one('repair.order', string="Repair Sequence")
    done = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string='Done',
        copy=False, default='no', required=True, tracking=True)
    notify_sent = fields.Boolean(copy=False)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.schedule.plan') or '/'
        return super(MaintenanceSchedulePlan, self).create(vals)
