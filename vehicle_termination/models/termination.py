from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class VehicleTermination(models.Model):
    _name = 'vehicle.termination'
    _description = 'vehicle.termination'
    _rec_name = 'partner_id'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submited', 'Submitted'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel')
    ], default='draft')
    partner_id = fields.Many2one('res.partner', 'Customer')
    mla_id = fields.Many2one('mla.data',
                             domain="[('partner_id', '=', partner_id),('state', 'in', ('active', 'to_expire'))]")
    vo_id = fields.Many2one('vehicle.order',
                            domain="[('mla_id', '=', mla_id),('state', 'in',('inprogress','confirmed'))]")
    car_ids = fields.One2many(related='vo_id.vehicle_car_ids')
    order_car_ids = fields.Many2many('vehicle.car.details', domain="[('id', 'in', car_ids)]")
    date = fields.Date('Termination date')

    def action_submit(self):
        self.state = 'submited'

    def action_approve(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancel'


class CarLine(models.Model):
    _inherit = 'vehicle.car.details'

    value = fields.Float('Termination Value', compute='get_termination_value')

    def get_termination_value(self):
        for rec in self:

            termination = self.env['vehicle.termination'].search([
                ('vo_id', '=', rec.vehicle_order_id.id),
                ('order_car_ids', 'in', rec.id),
            ], limit=1)
            if termination:
                termination_date = termination.date
                years_1 = rec.invoice_start_date + relativedelta(years=1)
                years_2 = rec.invoice_start_date + relativedelta(years=2)
                years_3 = rec.invoice_start_date + relativedelta(years=3)
                years_4 = rec.invoice_start_date + relativedelta(years=4)
                if termination_date <= years_1:
                    rec.value = 0
                elif termination_date < years_2:
                    rec.value = termination.mla_id.second_year_penality
                elif termination_date < years_3:
                    rec.value = termination.mla_id.third_year_penality
                elif termination_date < years_4:
                    rec.value = termination.mla_id.fourth_year_penality
            else:
                rec.value = 0
