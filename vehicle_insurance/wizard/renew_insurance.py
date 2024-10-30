# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
import datetime


class RenewVehicleInsurance(models.TransientModel):
    _name = "vehicle.insurance.renew"
    _description = "Renew Vehicle Insurance"

    insurance_id = fields.Many2one(comodel_name="vehicle.insurance", string="Insurance", required=False, )
    user_id = fields.Many2one('res.users', string='User', required=False, default=lambda self: self.env.user)
    date_from = fields.Date(string="Date From", required=True, )
    date_to = fields.Date(string="Insurance End date", compute="get_date_to")
    years_no = fields.Integer(string="No of years", required=True, )
    creation_date = fields.Date(string="Creation date", default=fields.Date.today())
    attachment = fields.Binary('Attachment', )

    @api.depends('date_from', 'years_no')
    def get_date_to(self):
        for rec in self:
            if rec.date_from and rec.years_no:
                rec.date_to = rec.date_from + relativedelta(years=rec.years_no)
            else:
                rec.date_to = False

    def action_update_insurance(self):
        # update Insurance
        for rec in self:
            # update Insurance
            rec.insurance_id.date_from = rec.date_from
            rec.insurance_id.date_to = rec.date_to
            if rec.date_to and rec.date_to > (datetime.date.today() + relativedelta(months=2)):
                rec.insurance_id.state = 'valid'
            # Create Insurance Line
            insurance_line_values = {
                'vehicle_insurance_id': rec.insurance_id.id,
                'user_id': rec.user_id.id,
                'creation_date': rec.creation_date,
                'date_from': rec.date_from,
                'date_to': rec.date_to,
                'attachment': rec.attachment,
                'years_no': rec.years_no,
            }
            self.env['vehicle.insurance.line'].create(insurance_line_values)
