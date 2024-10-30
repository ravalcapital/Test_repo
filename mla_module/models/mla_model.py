# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

STATES = [
    'draft',
    'to_sign',
    'active',
    'to_expire',
    'expired',
    'cancel',
]


class MlaModel(models.Model):
    _name = 'mla.data'
    _description = 'mla.data'
    _order = "seq_handle asc"

    name = fields.Char(required=True, string="Sequence", readonly=True, default=_('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_sign', 'To Sign'),
        ('active', 'Active'),
        ('to_expire', 'To Expire'),
        ('expired', 'Expired'),
        ('cancel', 'Cancelled'),
    ], default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string='Customer', domain=[('company_type', '=', 'company')])
    contact_id = fields.Many2one('res.partner')
    total_loss = fields.Integer()
    seq_handle = fields.Integer(string="", required=False, )

    initial_period = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date(compute='_get_end_date')
    type = fields.Selection([('long_term', 'Long Term'), ('short_term', 'Short Term')],
                            string='Type', required=True)
    auto_renewal = fields.Selection(
        selection=[('auto_renewal', 'Auto Renewal'), ('non_auto_renewal', 'Non Auto Renewal')],
        string="Auto Renewal", required=True)
    termination_notice = fields.Integer()
    payment_term_id = fields.Many2one('account.payment.term')
    daily_interest_charge = fields.Float('Delay Interest Percentage')
    # authorized tire charge
    first = fields.Integer()
    every_km = fields.Integer()

    # Insurance deductible
    per_accident_deduction = fields.Integer()
    per_third_party_liability = fields.Integer()
    # Early Termination Penalty
    second_year_penality = fields.Integer()
    third_year_penality = fields.Integer()
    fourth_year_penality = fields.Integer()

    # Traffic Tickets and violations
    admin_fees_inside_cairo = fields.Integer(string="Withdraw Licence Inside Cairo")
    admin_fees_outside_cairo = fields.Integer(string=" Withdraw Licence Outside Cairo")
    traffic_payment_term_id = fields.Many2one('account.payment.term')
    # Down Payment and Security Deposits
    security_deposit = fields.Integer()
    first_year_down_payment = fields.Integer()
    second_year_down_payment = fields.Integer()
    third_year_down_payment = fields.Integer()

    @api.model
    def create(self, vals):

        vals['name'] = _('New')
        return super(MlaModel, self).create(vals)

    def write(self, vals):
        if vals.get('name', _('New')) == _('New') and vals.get('state') == 'to_sign':
            vals['name'] = self.env['ir.sequence'].next_by_code('mla.sequence') or _('New')

        return super(MlaModel, self).write(vals)

    @api.constrains('type', 'initial_period')
    def _check_type_and_dates(self):
        if self.type == 'short_term' and self.initial_period > 12:
            raise ValidationError("Initial Period should not exceed 12")
        if self.type == 'long_term' and self.initial_period < 12:
            raise ValidationError("Initial Period should not less than 12")

    # def reminder_mla_action(self):
    #     print(f'in reminder_mla_action - self:{self}')
    #     reminder_mla = self.env['mla.data']
    #     reminder_mla_line_ids = reminder_mla.search([('state', '=', 'active')])
    #     for line in reminder_mla_line_ids:
    #         end_date_calc = line.end_date - relativedelta(months=line.termination_notice)
    #         if line.end_date and end_date_calc >= fields.Date.today():
    #             line.state = 'to_expire'

    def reminder_mla_action(self):
        reminder_mla = self.env['mla.data']
        reminder_mla_line_ids = reminder_mla.search([('state', '=', 'active')])
        for line in reminder_mla_line_ids:
            end_date_calc = line.end_date - relativedelta(months=line.termination_notice)
            # end_date_calc = line.end_date - relativedelta(months=1)
            if line.end_date and end_date_calc <= fields.Date.today():
                line.state = 'to_expire'

    def auto_renewal_mla(self):
        renewal_mla = self.env['mla.data']
        renewal_mla_line_ids = renewal_mla.search(
            [('auto_renewal', '=', 'auto_renewal'), ('end_date', '=', fields.Date.today())])
        for line in renewal_mla_line_ids:
            line.start_date = fields.Date.today()
            line.end_date = fields.Date.today() + relativedelta(months=line.initial_period)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return {
            'domain': {
                'contact_id': [('id', 'in', self.partner_id.child_ids.ids)]
            }
        }

    @api.onchange('initial_period', 'start_date')
    def _get_end_date(self):
        for rec in self:
            rec.end_date = False
            if rec.start_date and rec.initial_period:
                rec.end_date = rec.start_date + relativedelta(months=rec.initial_period)

    def next_stage(self):
        index = STATES.index(self.state)
        if index < (len(STATES) - 1):
            self.state = STATES[index + 1]

    def previos_stage(self):
        index = STATES.index(self.state)
        if index > 0:
            self.state = STATES[index - 1]
