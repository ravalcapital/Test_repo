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


class accounut_tax(models.Model):
    _inherit = 'account.tax'

    tax_type = fields.Char(string='ETA Tax Code', help='This is the type of tax according to egyptian tax authority')


class accounut_tax_group(models.Model):
    _inherit = 'account.tax.group'

    tax_type = fields.Char(string='ETA Tax Code',
                           help='This is the type of tax group (Parent) according to egyptian tax authority')
