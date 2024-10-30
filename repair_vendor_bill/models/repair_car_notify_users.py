# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class RepairCarNotifiedUsers(models.Model):
    _name = 'repair.car.notified.users'

    car_notified_users = fields.Many2many('res.users',string='Notified Users For Car')