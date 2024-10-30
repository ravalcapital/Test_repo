# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class RepairTireNotifiedUsers(models.Model):
    _name = 'repair.notified.users'

    notified_users = fields.Many2many('res.users',string='Notified Users For Tire')

