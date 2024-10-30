from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import time
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from dateutil.relativedelta import relativedelta
from odoo.http import request


class AccountMoveInherit(models.Model):
    _name = 'account.move.vehicle'

    vehicle_o_id = fields.Many2one(comodel_name="vehicle.order", string="", required=False, )

    state = fields.Selection(selection=[('draft', 'Draft'), ('posted', 'Posted'), ('cancel', 'Cancelled')],
                             string="Status", default="draft", related="move_id.state", readonly=False)

    invoice_date = fields.Date(related="move_id.invoice_date", readonly=False)
    amount_total = fields.Monetary(related="move_id.amount_total", required=False, )
    currency_id = fields.Many2one(comodel_name="res.currency", related="move_id.currency_id", string="",
                                  required=False, )
    move_id = fields.Many2one(comodel_name="account.move", string="invoice", required=False,
                              domain=[('move_type', '=', 'out_invoice')])


class VehicleOrderPayment(models.Model):
    _name = 'vehicle.order.payment'

    vehicle_id = fields.Many2one(comodel_name="vehicle.order")
    total_rent = fields.Float(string="Total Monthly Rent", required=False, )
    vat_id = fields.Many2one(comodel_name="account.tax", string="", required=False, )
    vehicle_licence = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle License Plate", required=False, )
    vehicle_car_details_id = fields.Many2one("vehicle.car.details", string="Car Details Seq")
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    total_km = fields.Float(string="Expected Total KM")
    invoice_id = fields.Many2one("account.move", string='Invoice')
    pool_millage = fields.Boolean(string='Pool Millage', related="vehicle_id.pool_millage", store=True)
    invoice_policy = fields.Selection(related="vehicle_id.invoice_policy", store=True,
                                      string="Invoice Policy")
    is_grouped = fields.Boolean("Is Grouped", copy=False)

    def create_invoice_action(self):
        print("x")


class VehicleOrder(models.Model):
    _name = 'vehicle.order'
    _rec_name = 'name'
    _order = "id desc"

    name = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection(selection=[('draft', 'Draft'), ('inprogress', 'Inprogress'), ('confirmed', 'Confirmed'),
                                        ('expired', 'Expired')],
                             string="Status", default="draft")
    customer_id = fields.Many2one(comodel_name="res.partner")
    product_id = fields.Many2one(comodel_name="product.product")
    make_id = fields.Many2one(comodel_name="fleet.vehicle.model.brand")
    km_year = fields.Float(string="Yearly limited KM per car", required=False, )
    year_id = fields.Many2one('fleet.vehicle.model.year')
    finance = fields.Char()
    services = fields.Char()
    insurance = fields.Char()
    long_term_rental = fields.Boolean(string="Long Term Rental")
    fuel_card = fields.Boolean(string="Fuel Card")
    material_damage = fields.Boolean(string="Vehicle Material Damage")
    licence_register = fields.Boolean(string="Licence Registration")
    maintenance = fields.Boolean(string="Maintenance")
    replace_vehicle = fields.Boolean(string="Replacement Vehicle")
    door_services = fields.Boolean(string="Door to Door Services")
    is_buy = fields.Boolean(string="Option To buy")
    third_party_Liability = fields.Boolean(string="Third Party Liability")
    is_insurance = fields.Boolean(string="Insurance")
    tyre_management = fields.Boolean(string="Tyre Management")
    road_assistance = fields.Boolean(string="Road Assistance")
    extra_km = fields.Float(string="Extra KM Rate")
    duration = fields.Float(string="Duration / Month")
    vo_start_date = fields.Date("Vehicle Order Start Date")
    vo_end_date = fields.Date("Vehicle Order End Date", compute='_compute_vo_end_date_period', store=True)


    @api.depends('vo_start_date')
    def _compute_vo_end_date_period(self):
        for record in self:
            months_no = int(record.duration)
            if record.vo_start_date:
                record.vo_end_date = record.vo_start_date + relativedelta(months=months_no)
            else:
                record.vo_end_date = record.vo_start_date

    no_Vehicles = fields.Integer(string="Number Of Vehicles", required=False, )
    order_id = fields.Many2one(comodel_name="sale.order", string="Related Sales")
    contact_id = fields.Many2one(comodel_name="res.partner")
    created_by = fields.Many2one(comodel_name="hr.employee")
    model_id = fields.Many2one(comodel_name="fleet.vehicle.model")
    total_km = fields.Float(required=False, string="Total KM For the VO Duration", compute="compute_total_km")
    vehicle_payments = fields.One2many(comodel_name="vehicle.order.payment", inverse_name="vehicle_id", )
    move_ids = fields.One2many(comodel_name="account.move.vehicle", inverse_name="vehicle_o_id", string="",
                               required=False, )
    terms_conditions = fields.Text(related='term_id.terms', string="Terms and Conditions")
    term_id = fields.Many2one(comodel_name="vo.term", string="", required=False, )
    unit_price = fields.Float(string="Monthly Rent")
    vat = fields.Many2one(comodel_name="account.tax", string="", required=False, )
    total_qty = fields.Float()
    currency = fields.Many2one(comodel_name="res.currency", string="", required=False,
                               default=lambda self: self.env.user.company_id.currency_id)
    transmition_type = fields.Selection(selection=[('automatic', 'Automatic'), ('manual', 'Manual')], default="manual")
    bank_id = fields.Many2one(comodel_name="res.bank", string="", required=False, )
    bank_account_id = fields.Many2one(comodel_name="res.partner.bank", string="", required=False, )
    invoice_every_months = fields.Integer(string="Invoice Every Months")
    invoice_policy = fields.Selection(selection=[('grouped', 'Grouped'), ('individual', 'Individual')],
                                      string="Invoice Policy")
    vehicle_car_ids = fields.One2many('vehicle.car.details', 'vehicle_order_id', string="Car Details")
    option_to_puy = fields.Selection([('operating_lease', 'Operating Lease'), ('lease_to_own', 'Lease to Own')],
                                     string='Leasing Type')
    contract_term = fields.Selection([('long_term', 'Long Term'), ('short_term', 'Short Term')],
                                     string='Contract Term')
    millage_calculation = fields.Selection([('pool', 'Pool'), ('limited_km', 'Limited KM')],
                                           string='Millage Calculation')
    total_pool_millage = fields.Float(string='Total Pool Millage')
    pool_millage = fields.Boolean(string='Pool Millage', copy=False)
    is_sent = fields.Boolean(string="", )
    journal_id = fields.Many2one('account.journal', string='Journal')

    # mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", related="order_id.mla_id", store=True)

    @api.constrains('no_Vehicles', 'vehicle_car_ids')
    def _check_vehicle_car_details_lines(self):
        for rec in self:
            if len(rec.vehicle_car_ids) > rec.no_Vehicles:
                raise ValidationError("Car Details Lines should not exceed Vehicle Order Number Of Vehicles")
            total_km = 0.0
            for line in rec.vehicle_car_ids:
                total_km += line.total_km
                # if line.model_m_id != rec.model_id:
                #     raise ValidationError("Car Details Model should be the same as Vehicle Order Model")

            # if total_km > rec.total_km:
            #     raise ValidationError("Sum Total KM of Car Details Lines should not exceed Vehicle Order Total KM")

    def check_vo_end_date(self):
        links = ''
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.sudo().id, self.sudo()._name)
        links += base_url

        vehicle_orders = self.env['vehicle.order'].search([('vo_end_date', '!=', False), ('is_sent', '=', False)])
        today = fields.Date.today()
        for vo in vehicle_orders:
            today_str = fields.Date.from_string(today)
            approve = fields.Date.from_string(vo.vo_end_date)
            difference = relativedelta(approve, today_str)
            mail_template = self.env.ref('vehicle_order.vo_email_template_id')

            print(difference, today_str, vo.vo_end_date, difference.days, difference.months)
            if difference.days == 30 and difference.months == 0:
                mail = mail_template.send_mail(vo.id)
                vo.is_sent = True

            if difference.days == 0 and difference.months == 1:
                mail = mail_template.send_mail(vo.id)
                vo.is_sent = True

            # vals = {
            #     'author_id': self.env.user.id,
            #     'body_html': 'Dear %s </br> your vehicle order number %s is to be expired on %s Contact us for renewal' % (
            #         vo.customer_id.name, vo.name, vo.vo_end_date),
            #     'subject': 'Notification: Vehicle Order %s Ending in 30 days' % vo.name,
            #     'email_from': self.env.user.email_formatted,
            #     'email_to': 'christinefayez44@gmail.com',
            #     'auto_delete': True,
            #     'is_notification': True,
            #     'message_type': 'notification',
            #
            # }
            # mail = self.env['mail.mail'].sudo().create(vals)
            # mail.send()

    @api.model
    def create(self, vals):
        vals['name'] = _('New')
        vals['terms_conditions'] = self.env['ir.config_parameter'].sudo().get_param('base_setup.terms_conditions')
        return super(VehicleOrder, self).create(vals)

    def write(self, vals):
        if vals.get('name', _('New')) == _('New') and vals.get('state') == 'inprogress':
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.order') or _('New')
            vals['terms_conditions'] = self.env['ir.config_parameter'].sudo().get_param('base_setup.terms_conditions')

        return super(VehicleOrder, self).write(vals)

    def inprogress_button(self):
        self.write({
            'state': "inprogress"
        })

    def expired_button(self):
        for rec in self:
            if rec.vehicle_car_ids:
                for car in rec.vehicle_car_ids:
                    car.fleet_licence_plate_id.write({'vo_id':None,'mla_id':None,'customer_id':None })

            rec.write({
                'state': "expired"
            })


    # def expired_button(self):
    #     for rec in self:
    #         if rec.vehicle_car_ids:
    #             for car in rec.vehicle_car_ids:
    #                 car.fleet_licence_plate_id.write({'vo_id': None, 'mla_id': None, 'customer_id': None})
    #         if rec.vehicle_payments:
    #             last_vehicle_payments = self.env['vehicle.order.payment'].search([('id','in',rec.vehicle_payments.ids)],order='date_from desc',limit=1)
    #             if not last_vehicle_payments.invoice_id:
    #                 raise ValidationError('There are Monthly Payments Or Milage Due...')
    #
    #         rec.write({
    #             'state': "expired"
    #         })


    def confirmed_button(self):
        for rec in self:
            rec.write({
                'state': "confirmed"
            })
            for car in rec.vehicle_car_ids:
                car.fleet_licence_plate_id.write({
                    'vo_id': rec.id,
                    'mla_id':rec.mla_id.id,
                    'customer_id':rec.customer_id.id
                })


    def bank_details_letter(self):
        return self.env.ref('vehicle_order.print_bank_details_report_id').report_action(self)

    @api.depends('duration', 'no_Vehicles',
                 'km_year')
    def compute_total_km(self):
        for rec in self:
            rec.total_km = rec.km_year * (
                    rec.duration / 12) * rec.no_Vehicles

    def create_invoice_action(self):
        print("x")


class VehicleCarDetails(models.Model):
    _name = 'vehicle.car.details'
    _description = 'Cars Details'

    name = fields.Char(string="Cars Details Seq", required=True, readonly=True, default='/', copy=False)
    fleet_licence_plate_id = fields.Many2one(comodel_name="fleet.vehicle", string="Fleet License Plate",
                                             required=False, )
    model_m_id = fields.Many2one("fleet.vehicle.model", string="Models", related="fleet_licence_plate_id.model_id",
                                 store=True)
    model_id = fields.Many2one("fleet.vehicle.model", string="Models", related="vehicle_order_id.model_id",
                               store=True)
    invoice_start_date = fields.Date("Invoice Start Date", default=lambda self: fields.Date.today(),
                                     required=True, )
    no_of_invoices = fields.Float(string="No Of Invoices", compute="compute_no_of_invoices")
    total_km = fields.Float(string="Last KM Reading")
    vehicle_order_id = fields.Many2one('vehicle.order', string='order')
    vehicle_order_payment_ids = fields.One2many('vehicle.order.payment', 'vehicle_car_details_id',
                                                string='Monthly Payments')
    pool_millage = fields.Boolean(string='Pool Millage', related="vehicle_order_id.pool_millage", store=True)
    invoice_policy = fields.Selection(related="vehicle_order_id.invoice_policy", store=True,
                                      string="Invoice Policy")
    vehicle_ids = fields.Many2many('fleet.vehicle', string='Vehicle', compute="get_all_vehicles")
    initial_km = fields.Float(string="Initial KM")
    outsource_serial = fields.Char(string="OutSource Serial", required=False, )

    @api.depends('vehicle_order_id', 'vehicle_order_id.model_id')
    def get_all_vehicles(self):
        for rec in self:
            vehicle_list = []
            car_details_obj = self.env['vehicle.car.details'].search([])
            for line in car_details_obj:
                if line.vehicle_order_id.state in ('inprogress', 'confirmed'):
                    vehicle_list.append(line.fleet_licence_plate_id.id)
            # all_vehicle = self.env['fleet.vehicle'].search(
            #     [('id', 'not in', vehicle_list), ('model_id', '=', rec.vehicle_order_id.model_id.id)]).ids
            all_vehicle = self.env['fleet.vehicle'].search(
                [('id', 'not in', vehicle_list)]).ids

            rec.vehicle_ids = [(6, 0, all_vehicle)]

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('/'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.car.details') or '/'
        return super(VehicleCarDetails, self).create(vals)

    @api.depends('vehicle_order_id', 'vehicle_order_id.duration', 'vehicle_order_id.invoice_every_months')
    def compute_no_of_invoices(self):
        for rec in self:
            if rec.vehicle_order_id.invoice_every_months != 0:
                rec.no_of_invoices = rec.vehicle_order_id.duration / rec.vehicle_order_id.invoice_every_months
            else:
                rec.no_of_invoices = 0.0

    def unlink(self):
        for line in self:
            for pay in line.vehicle_order_payment_ids:
                if line.id == pay.vehicle_car_details_id.id:
                    pay.unlink()
        return super(VehicleCarDetails, self).unlink()

    def generate_pre_invoice_lines_action(self):
        monthly_payment_km_month = 0.0
        for rec in self:
            if not rec.vehicle_order_id.invoice_every_months:
                raise ValidationError(_('Please set Invoice Every Months for Vehicle Order.'))
            else:
                invoice_every_months = rec.vehicle_order_id.invoice_every_months
            if not rec.vehicle_order_id.duration:
                raise ValidationError(_('Please set Duration for Vehicle Order.'))
            monthly_payment_obj = self.env['vehicle.order.payment']
            start_date = rec.invoice_start_date
            monthly_payment_km_inc = 0
            monthly_payment_km = 0
            # monthly_payment_km_month = (rec.vehicle_order_id.total_km / rec.vehicle_order_id.duration) * invoice_every_months

            monthly_payment_km_month = (rec.vehicle_order_id.km_year / 12) * invoice_every_months
            if rec.initial_km:
                monthly_payment_km += rec.initial_km

            for pay_no in range(0, int(rec.no_of_invoices)):
                # if monthly_payment_km_inc == 0:
                #     monthly_payment_km = monthly_payment_km_month
                # else:

                monthly_payment_km += monthly_payment_km_month
                date_from = start_date
                date_to = date_from + relativedelta(months=invoice_every_months) - relativedelta(days=1)
                start_date = date_to + relativedelta(days=1)
                monthly_payment_line = {
                    'date_from': date_from.strftime('%Y-%m-%d'),
                    'date_to': date_to.strftime('%Y-%m-%d'),
                    'vehicle_id': rec.vehicle_order_id.id,
                    'total_rent': rec.vehicle_order_id.unit_price,
                    'vat_id': rec.vehicle_order_id.vat.id,
                    'vehicle_car_details_id': rec.id,
                    'vehicle_licence': rec.fleet_licence_plate_id.id,
                    'total_km': monthly_payment_km,
                }

                monthly_payment_obj.create(monthly_payment_line)

                monthly_payment_km_inc += invoice_every_months
                pay_no += 1
