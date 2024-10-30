# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2019-TODAY .
#    Author: Plementus <https://plementus.com>
#    Contributor: Mario Roshdy <m.roshdy@plementus.com>
#    Contributor: Karim Jaber <kareem@plementus.com>
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################

from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = 'res.partner'

    eta_code = fields.Char(string='ETA Code (TAX ID)', help='This is the code (TAX ID) of partner according to egyptian tax authority')
    eta_activity_type = fields.Char('ETA Activity Code',
                                    help='This is the activity type of partner according to egyptian tax authority')
    building_no = fields.Char('Building No.')
    floor = fields.Char('Floor')
    room = fields.Char('Room')
    landmark = fields.Char('Landmark')
    additional_information = fields.Char('Additional Information')
    national_id = fields.Char('National ID')
