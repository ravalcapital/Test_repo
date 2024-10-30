from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

import numpy as np  # version: 1.16.2
import pandas as pd  # version: 0.25.1
import calendar
from datetime import datetime


class VehicleCarDetails(models.Model):
    _inherit = 'vehicle.car.details'

    no_of_invoices_millage = fields.Float(compute='compute_no_of_invoices_millage', string='NO OF Invoices Extra KM')

    @api.depends('vehicle_order_id', 'vehicle_order_id.duration', 'vehicle_order_id.millage_invoice_every_months')
    def compute_no_of_invoices_millage(self):
        for rec in self:
            if rec.vehicle_order_id.millage_invoice_every_months != 0:
                rec.no_of_invoices_millage = rec.vehicle_order_id.duration / rec.vehicle_order_id.millage_invoice_every_months
            else:
                rec.no_of_invoices_millage = 0.0

    def generate_pre_invoice_lines_action(self):
        print(f'in generate_pre_invoice_lines_action - in vo_monthly_payment_edit ')
        monthly_payment_km_month = 0.0
        millage_monthly_payment_km_month = 0.0
        is_one = False
        for rec in self:
            if not rec.vehicle_order_id.invoice_every_months:
                raise ValidationError(_('Please set Invoice Every Months for Vehicle Order.'))
            else:
                invoice_every_months = rec.vehicle_order_id.invoice_every_months
            if not rec.vehicle_order_id.duration:
                raise ValidationError(_('Please set Duration for Vehicle Order.'))
            monthly_payment_obj = self.env['vehicle.order.payment']
            millage_monthly_payment_obj = self.env['millage.vehicle.payment']
            start_date = rec.invoice_start_date
            vo_end_date = rec.end_date
            print(f'in generate_pre_invoice_lines_action - vo_end_date:{vo_end_date}')
            monthly_payment_km_inc = 0
            monthly_payment_km = 0
            date_to_diff = 0
            diff_first_m = False

            date_to = False

            monthly_payment_km_month = (rec.vehicle_order_id.km_year / 12) * invoice_every_months
            if rec.initial_km:
                monthly_payment_km += rec.initial_km

            for pay_no in range(0, int(rec.no_of_invoices)):

                monthly_payment_km += monthly_payment_km_month
                date_from = start_date
                date_to = date_from + relativedelta(months=invoice_every_months) - relativedelta(days=1)
                if date_from.day > 2 and is_one == False:
                    date_to = date_from.replace(day=calendar.monthrange(date_from.year, date_from.month)[1])
                    date_to_diff = (rec.invoice_start_date + relativedelta(months=invoice_every_months)) - date_from
                    diff_first_m = date_to - date_from
                    is_one = True

                start_date = date_to + relativedelta(days=1)
                print('date_to',date_to)
                ddate_to = date_to.strftime('%Y-%m-%d')
                print(f'ddate_to 2222:{ddate_to}')
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
                print(f'monthly_payment_line :{monthly_payment_line} - ddate_to :{ddate_to} - vo_end_date ::{vo_end_date}')
                monthly_payment_obj.create(monthly_payment_line)

                monthly_payment_km_inc += invoice_every_months
                monthly_payment_km_inc += invoice_every_months
                pay_no += 1

            if date_to_diff:
                days = date_to_diff.days - diff_first_m.days + 1
                date_to = date_to + relativedelta(days=days) - relativedelta(days=1)

                monthly_payment_line = {
                    'date_from': start_date.strftime('%Y-%m-%d'),
                    'date_to': date_to.strftime('%Y-%m-%d'),
                    'vehicle_id': rec.vehicle_order_id.id,
                    'total_rent': rec.vehicle_order_id.unit_price,
                    'vat_id': rec.vehicle_order_id.vat.id,
                    'vehicle_car_details_id': rec.id,
                    'vehicle_licence': rec.fleet_licence_plate_id.id,
                    'total_km': monthly_payment_km,
                }
                line = monthly_payment_obj.create(monthly_payment_line)

        self.generate_pre_invoice_line_millage()

    def generate_pre_invoice_line_millage(self):
        is_one = False
        for rec in self:
            if not rec.vehicle_order_id.millage_invoice_every_months:
                raise ValidationError(_('Please set Invoice Every Months for Vehicle Order.'))
            else:
                invoice_every_months = rec.vehicle_order_id.millage_invoice_every_months
            if not rec.vehicle_order_id.duration:
                raise ValidationError(_('Please set Duration for Vehicle Order.'))
            monthly_payment_obj = self.env['vehicle.order.payment']
            millage_monthly_payment_obj = self.env['millage.vehicle.payment']
            start_date = rec.invoice_start_date
            monthly_payment_km_inc = 0
            monthly_payment_km = 0
            date_to_diff = 0
            diff_first_m = False

            date_to = False

            monthly_payment_km_month = (rec.vehicle_order_id.km_year / 12) * invoice_every_months
            if rec.initial_km:
                monthly_payment_km += rec.initial_km

            for pay_no in range(0, int(rec.no_of_invoices_millage)):

                monthly_payment_km += monthly_payment_km_month
                date_from = start_date
                date_to = date_from + relativedelta(months=invoice_every_months) - relativedelta(days=1)
                if date_from.day > 2 and is_one == False:
                    date_to = date_from.replace(day=calendar.monthrange(date_from.year, date_from.month)[1])
                    date_to_diff = (rec.invoice_start_date + relativedelta(months=invoice_every_months)) - date_from
                    diff_first_m = date_to - date_from
                    is_one = True
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
                millage_monthly_payment_obj.create(monthly_payment_line)

                monthly_payment_km_inc += invoice_every_months
                monthly_payment_km_inc += invoice_every_months
                pay_no += 1
            if date_to_diff:
                days = date_to_diff.days - diff_first_m.days + 1
                date_to = date_to + relativedelta(days=days) - relativedelta(days=1)
                monthly_payment_line = {
                    'date_from': start_date.strftime('%Y-%m-%d'),
                    'date_to': date_to.strftime('%Y-%m-%d'),
                    'vehicle_id': rec.vehicle_order_id.id,
                    'total_rent': rec.vehicle_order_id.unit_price,
                    'vat_id': rec.vehicle_order_id.vat.id,
                    'vehicle_car_details_id': rec.id,
                    'vehicle_licence': rec.fleet_licence_plate_id.id,
                    'total_km': monthly_payment_km,
                }
                line = millage_monthly_payment_obj.create(monthly_payment_line)


class VehicleCarDetailsMillage(models.Model):
    _name = 'millage.vehicle.payment'
    _description = 'Millage Cars Details'

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
    # pool_millage = fields.Boolean(string='Pool Millage', store=True)
    invoice_policy = fields.Selection(related="vehicle_id.millage_invoice_policy", store=True,
                                      string="Invoice Policy")
    is_grouped = fields.Boolean("Is Grouped", copy=False)
    km_reading = fields.Float(string="Consumed KM")
    extra_km = fields.Float(string="Extra KM")
    no_of_days = fields.Integer(compute='clc_no_of_days')
    total_rent = fields.Float(string="Total Monthly Rent", required=False, compute='clc_monthly_rent', readonly=0)

    @api.depends('no_of_days')
    def clc_monthly_rent(self):
        for rec in self:
            start_dt = fields.Datetime.from_string(rec.date_from)
            finish_dt = fields.Datetime.from_string(rec.date_to + relativedelta(days=1))
            difference = relativedelta(finish_dt, start_dt)
            if rec.vehicle_id.unit_price > 0 and difference.months == 0:
                rec.total_rent = (rec.vehicle_id.unit_price / 30) * rec.no_of_days

            elif rec.vehicle_id.unit_price > 0 and difference.months > 0:
                rec.total_rent = rec.vehicle_id.unit_price * rec.vehicle_id.millage_invoice_every_months

            else:
                rec.total_rent = 0

    def clc_no_of_days(self):
        for rec in self:
            rec.no_of_days = 0
            if rec.date_to and rec.date_from:
                rec.no_of_days = (rec.date_to - rec.date_from).days

    def create_invoice_action(self):
        print(f'in create_invoice_action - of millage.vehicle.payment')
        for rec in self:
            if not rec.vehicle_id.product_id:
                raise ValidationError('Please Select Product for Vehicle Order')
            if not rec.vehicle_id.journal_id:
                raise ValidationError('Please Select Journal for Vehicle Order')
            if not rec.vehicle_id.customer_id:
                raise ValidationError('Please Select Customer for Vehicle Order')

            vat_id = []
            if rec.vat_id:
                vat_id.append((4, rec.vat_id.id))
            print(f'in create_invoice_action - of millage.vehicle.payment - vat_id :{vat_id}')
            lot_id = []
            vehicle_licence = []
            # product_object2 = False
            # product_extra2 = self.env['product.product'].search(
            #     [('extra_km', '=', True), ('detailed_type', '=', 'service')], limit=1)
            # print(f'product_extra2111 is kkkkkkkk:{product_extra2}')
            # if len(product_extra2) > 0:
            #     product_object2 = product_extra2
            #     print(f'product_object2a21555 is kkkkkkkk:{product_object2}')
            # else:
            #     product_obj2 = self.env['product.product'].create(
            #         {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
            #     print(f'product_obj2 agyerrrr created : {product_obj2}')
            # print(f'product_object2 6666666 is kkkkkkkk:{product_object2}')
            if rec.vehicle_licence:
                vehicle_licence.append((4, rec.vehicle_licence.id))
                print(f'in create_invoice_action - of millage.vehicle.payment - vehicle_licence :{vehicle_licence}')
                if rec.vehicle_licence.lot_id:
                    lot_id.append((4, rec.vehicle_licence.lot_id.id))
                    print(f'in create_invoice_action - of millage.vehicle.payment - lot_id :{lot_id}')

            if rec.vehicle_id.extra_km > 0:
                # product_obj = self.env['product.product'].create(
                #     {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                product_obj = False
                product_obj = self.env['product.product'].search(
                    [('extra_km', '=', True), ('detailed_type', '=', 'service')], limit=1)
                print(f'product_obj searcheddddddddd :{product_obj}')
                if not product_obj:
                    product_obj = self.env['product.product'].create(
                        {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                    print(f'product_obj creaaaaaaaateddddd :{product_obj}')
                print(
                    f'in create_invoice_action - of millage.vehicle.payment -rec.vehicle_id.extra_km >0 =  product_obj :{product_obj}')
                account_move_vals = {
                        "partner_id": rec.vehicle_id.customer_id.id,
                        "journal_id": rec.vehicle_id.journal_id.id,
                        "vo_id": rec.vehicle_id.id,
                        "mla_id": rec.vehicle_id.mla_id.id,
                        'invoice_date': rec.create_date,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [
                            (0, 0,
                             {
                                 "product_id": product_obj.id,
                                 "quantity": rec.extra_km,
                                 "price_unit": rec.vehicle_id.extra_km,
                                 "name": rec.vehicle_id.product_id.display_name,
                                 "vehicle_licence_ids": vehicle_licence,

                                 # "vehicle_licence": rec.vehicle_licence.id,
                                 "vehicle_car_details_ids": [(4, rec.vehicle_car_details_id.id)],

                                 # "vehicle_car_details_id": rec.vehicle_car_details_id.id,
                                 "date_from": rec.date_from,
                                 "date_to": rec.date_to,
                                 "total_km": rec.total_km,
                                 "millage_invoice_ids": [(4, rec.id)],
                                 "km_reading": rec.km_reading,
                                 "extra_km": rec.extra_km,
                             })
                        ]
                    }
                print(f'account_move_vals :{account_move_vals}')
                out_invoice_obj = self.env["account.move"].create(account_move_vals)
                print(f'out_invoice_obj :{out_invoice_obj}')
                rec.invoice_id = out_invoice_obj


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    millage_invoice_ids = fields.Many2many(comodel_name="millage.vehicle.payment", relation="vo_millage_rel",
                                           column1="millage_payment_col1", column2="millage_payment_col2",
                                           string="Millage", )


class VehicleOrder(models.Model):
    _inherit = 'vehicle.order'

    millage_invoice_every_months = fields.Integer(string="Millage Invoice Every Months")
    invoice_every_months = fields.Integer(string="Rent Invoice Every Months")

    millage_car_details_ids = fields.One2many(comodel_name="millage.vehicle.payment", inverse_name="vehicle_id",
                                              string="", required=False, )

    millage_invoice_policy = fields.Selection(string="Millage Invoice Policy",
                                              selection=[('grouped', 'Grouped'), ('individual', 'Individual')],
                                              required=False, )

    limited_poolmillage_extra = fields.Float(string="Limited Pool Millage",
                                             compute="compute_limited_pool_millage_extra_km")

    @api.depends('millage_invoice_policy')
    @api.onchange('millage_invoice_policy')
    def _onchange_millage_invoice_policy(self):
        for rec in self:
            if rec.millage_invoice_policy == 'grouped':
                rec.pool_millage = True
            else:
                rec.pool_millage = False

    def expired_button(self):
        for rec in self:
            if rec.vehicle_car_ids:
                for car in rec.vehicle_car_ids:
                    car.fleet_licence_plate_id.write({'vo_id': None, 'mla_id': None, 'customer_id': None})
            if rec.vehicle_payments:
                last_vehicle_payments = self.env['vehicle.order.payment'].search([('id','in',rec.vehicle_payments.ids)],order='date_from desc',limit=1)
                if not last_vehicle_payments.invoice_id:
                    raise ValidationError('There are Monthly Payments Due...')
            if rec.millage_car_details_ids:
                last_millage_vehicle_payment = self.env['millage.vehicle.payment'].search(
                    [('id', 'in', rec.millage_car_details_ids.ids)], order='date_from desc', limit=1)
                if not last_millage_vehicle_payment.invoice_id:
                    raise ValidationError('There are Milage Due Due...')

            rec.write({
                'state': "expired"
            })

    @api.depends('km_year', 'millage_invoice_policy', 'no_Vehicles')
    def compute_limited_pool_millage_extra_km(self):
        for rec in self:
            if rec.km_year > 0:
                rec.limited_poolmillage_extra = (rec.km_year / 12) * rec.millage_invoice_every_months * rec.no_Vehicles
            else:
                rec.limited_poolmillage_extra = 0.0

    def update_odometer_value(self):
        for rec in self:
            for line in rec.vehicle_car_ids:
                odometer_obj = self.env['fleet.vehicle.odometer'].search(
                    [('vehicle_id', '=', line.fleet_licence_plate_id.id)], order='date desc , value desc', limit=1)
                line.total_km = odometer_obj.value

            for pay in rec.vehicle_payments:
                odometer = self.env['fleet.vehicle.odometer'].search([
                    ('date', '>=', pay.date_from), ('date', '<=', pay.date_to),
                    ('vehicle_id', '=', pay.vehicle_licence.id),
                    ('vo_id', '=', rec.id)
                ], order='date desc', limit=1)
                if odometer:
                    pay.km_reading = odometer.value
                else:
                    pay.km_reading = 0.0
                pay.extra_km = 0

            for pay_mill in rec.millage_car_details_ids:
                odometer = self.env['fleet.vehicle.odometer'].search([
                    ('date', '>=', pay_mill.date_from), ('date', '<=', pay_mill.date_to),
                    ('vehicle_id', '=', pay_mill.vehicle_licence.id),
                    ('vo_id', '=', rec.id)
                ], order='date desc', limit=1)
                if odometer:
                    pay_mill.km_reading = odometer.value
                else:
                    pay_mill.km_reading = 0.0
                # extra_km = pay.km_reading - rec.limited_monthly_km
                extra_km = pay_mill.km_reading - pay_mill.total_km
                if extra_km > 0:
                    pay_mill.extra_km = extra_km
                else:
                    pay_mill.extra_km = 0.0

    def create_invoice_action(self):
        for vo in self:
            if not vo.product_id:
                raise ValidationError('Please Select Product for Vehicle Order')
            if not vo.journal_id:
                raise ValidationError('Please Select Journal for Vehicle Order')
            if not vo.customer_id:
                raise ValidationError('Please Select Customer for Vehicle Order')
            all_vehicles_date = []
            all_payment_line = []
            total_extra_km = 0.0
            for rec in vo.vehicle_payments:
                if rec.is_grouped == True and not rec.invoice_id:
                    all_vehicles_date.append(rec.date_from)
                    if vo.pool_millage == True:
                        total_extra_km += rec.extra_km
                        all_payment_line.append(rec.id)
            if total_extra_km > vo.limited_poolmillage_extra:
                total_extra_km_pool = total_extra_km - vo.limited_poolmillage_extra
            else:
                total_extra_km_pool = total_extra_km
            set_all_vehicles = set(all_vehicles_date)
            if len(set_all_vehicles) > 1:
                raise ValidationError('Please Select lines with same Dates')

            if vo.extra_km > 0:
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": vo.customer_id.id,
                        "journal_id": vo.journal_id.id,
                        "vo_id": vo.id,
                        "mla_id": vo.mla_id.id,
                        'invoice_date': vo.create_date,
                        "move_type": "out_invoice",
                        "invoice_line_ids": []})

            else:
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": vo.customer_id.id,
                        "journal_id": vo.journal_id.id,
                        "vo_id": vo.id,
                        'invoice_date': vo.create_date,
                        "mla_id": vo.mla_id.id,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [],
                    })
            out_invoice_obj_indvidual2_flag = False
            for rec in vo.vehicle_payments:
                total_rent = 0.0
                total_km = 0.0
                km_reading = 0.0
                extra_km = 0.0
                vehicle_car_details_id = []
                vehicle_licence = False
                tax_ids = []
                vo_payment_ids = []
                all_vehicles = []
                lot_ids = []

                if rec.is_grouped == True and not rec.invoice_id:
                    all_vehicles_date.append(rec.date_from)
                    if rec.vehicle_licence:
                        all_vehicles.append(rec.vehicle_licence.id)
                        if rec.vehicle_licence.lot_id:
                            lot_ids.append(rec.vehicle_licence.lot_id.id)
                    total_rent += rec.total_rent
                    vehicle_licence = rec.vehicle_licence
                    vehicle_car_details_id.append(rec.vehicle_car_details_id.id)
                    product_obj = False
                    product_rent = self.env['product.product'].search(
                        [('is_rent', '=', True), ('detailed_type', '=', 'service')], limit=1)
                    if len(product_rent) > 0:
                        product_obj = product_rent
                    else:
                        product_obj = self.env['product.product'].create(
                            {'name': 'Rent', 'is_rent': True, 'detailed_type': 'service'})

                    date_from = rec.date_from
                    date_to = rec.date_to
                    total_km += rec.total_km
                    km_reading += rec.km_reading
                    extra_km += rec.extra_km
                    if rec.vat_id:
                        tax_ids.append(rec.vat_id.id)
                    vo_payment_ids.append(rec.id)
                    if vo.extra_km > 0:
                        if vo.pool_millage != True:

                            out_invoice_obj.invoice_line_ids = [
                                (0, 0,
                                 {
                                     "product_id": product_obj.id,
                                     "name": product_obj.display_name,
                                     "lot_ids": [(6, 0, lot_ids)],
                                     "quantity": 1,
                                     "price_unit": total_rent,
                                     "vehicle_licence_ids": [(6, 0, all_vehicles)],
                                     "vehicle_car_details_ids": [(6, 0, vehicle_car_details_id)],
                                     "date_from": date_from,
                                     "date_to": date_to,
                                     "total_km": total_km,
                                     "km_reading": km_reading,
                                     "extra_km": extra_km,
                                     "vo_payment_ids": [(6, 0, vo_payment_ids)],
                                     "tax_ids": [(6, 0, tax_ids)],
                                 },
                                 ),
                            ]

                            if rec.is_grouped == True and not rec.invoice_id:
                                rec.invoice_id = out_invoice_obj.id
                        else:
                            if vo.invoice_policy == 'grouped':
                                there_is_km = []
                                for inv_line in out_invoice_obj.invoice_line_ids:
                                    if inv_line.name == 'Extra KM':
                                        there_is_km.append(inv_line)
                                if not there_is_km:
                                    out_invoice_obj.invoice_line_ids = [
                                        (0, 0,
                                         {
                                             "product_id": product_obj.id,
                                             "name": product_obj.display_name,
                                             "lot_ids": [(6, 0, lot_ids)],
                                             "quantity": 1,
                                             "price_unit": total_rent,
                                             "vehicle_licence_ids": [(6, 0, all_vehicles)],
                                             "vehicle_car_details_ids": [(6, 0, vehicle_car_details_id)],
                                             "date_from": date_from,
                                             "date_to": date_to,
                                             "total_km": total_km,
                                             "km_reading": km_reading,
                                             "extra_km": extra_km,
                                             "vo_payment_ids": [(6, 0, vo_payment_ids)],
                                             "tax_ids": [(6, 0, tax_ids)],
                                         },
                                         ),
                                    ]
                                else:
                                    out_invoice_obj.invoice_line_ids = [
                                        (0, 0,
                                         {
                                             "product_id": product_obj.id,
                                             "name": product_obj.display_name,
                                             "lot_ids": [(6, 0, lot_ids)],
                                             "quantity": 1,
                                             "price_unit": total_rent,
                                             "vehicle_licence_ids": [(6, 0, all_vehicles)],
                                             "vehicle_car_details_ids": [(6, 0, vehicle_car_details_id)],
                                             "date_from": date_from,
                                             "date_to": date_to,
                                             "total_km": total_km,
                                             "km_reading": km_reading,
                                             "extra_km": extra_km,
                                             "vo_payment_ids": [(6, 0, vo_payment_ids)],
                                             "tax_ids": [(6, 0, tax_ids)],
                                         },
                                         )
                                    ]
                                if rec.is_grouped == True and not rec.invoice_id:
                                    rec.invoice_id = out_invoice_obj.id


                            else:
                                there_is_km = []
                                for inv_line in out_invoice_obj.invoice_line_ids:
                                    if inv_line.name == 'Extra KM':
                                        there_is_km.append(inv_line)
                                if not there_is_km:

                                    out_invoice_obj_indvidual = self.env["account.move"].create(
                                        {
                                            "partner_id": vo.customer_id.id,
                                            "journal_id": vo.journal_id.id,
                                            "vo_id": vo.id,
                                            "mla_id": vo.mla_id.id,
                                            'invoice_date': vo.create_date,
                                            "move_type": "out_invoice",
                                            "invoice_line_ids": [(0, 0,
                                                                  {
                                                                      "product_id": product_obj.id,
                                                                      "name": product_obj.display_name,
                                                                      "lot_ids": [(6, 0, lot_ids)],
                                                                      "quantity": 1,
                                                                      "price_unit": total_rent,
                                                                      "vehicle_licence_ids": [(6, 0, all_vehicles)],
                                                                      "vehicle_car_details_ids": [
                                                                          (6, 0, vehicle_car_details_id)],
                                                                      "date_from": date_from,
                                                                      "date_to": date_to,
                                                                      "total_km": total_km,
                                                                      "km_reading": km_reading,
                                                                      "extra_km": extra_km,
                                                                      "vo_payment_ids": [(6, 0, vo_payment_ids)],
                                                                      "tax_ids": [(6, 0, tax_ids)],
                                                                  },
                                                                  ), ]})
                                    if not out_invoice_obj_indvidual2_flag:
                                        out_invoice_obj_indvidual2 = self.env["account.move"].create(
                                            {
                                                "partner_id": vo.customer_id.id,
                                                "journal_id": vo.journal_id.id,
                                                "vo_id": vo.id,
                                                "mla_id": vo.mla_id.id,
                                                'invoice_date': vo.create_date,
                                                "move_type": "out_invoice",
                                            })
                                        out_invoice_obj_indvidual2_flag = out_invoice_obj_indvidual2
                                        vo.extra_km_invoice_ids = [(4, out_invoice_obj_indvidual2.id)]

                                else:
                                    out_invoice_obj_indvidual = self.env["account.move"].create(
                                        {
                                            "partner_id": vo.customer_id.id,
                                            "journal_id": vo.journal_id.id,
                                            "vo_id": vo.id,
                                            "mla_id": vo.mla_id.id,
                                            'invoice_date': vo.create_date,
                                            "move_type": "out_invoice",
                                            "invoice_line_ids": [(0, 0,
                                                                  {
                                                                      "product_id": product_obj.id,
                                                                      "name": product_obj.display_name,
                                                                      "lot_ids": [(6, 0, lot_ids)],
                                                                      "quantity": 1,
                                                                      "price_unit": total_rent,
                                                                      "vehicle_licence_ids": [(6, 0, all_vehicles)],
                                                                      "vehicle_car_details_ids": [
                                                                          (6, 0, vehicle_car_details_id)],
                                                                      "date_from": date_from,
                                                                      "date_to": date_to,
                                                                      "total_km": total_km,
                                                                      "km_reading": km_reading,
                                                                      "extra_km": extra_km,
                                                                      "vo_payment_ids": [(6, 0, vo_payment_ids)],
                                                                      "tax_ids": [(6, 0, tax_ids)],
                                                                  },
                                                                  ), ]})

                                if rec.is_grouped == True and not rec.invoice_id:
                                    rec.invoice_id = out_invoice_obj_indvidual.id

                    else:
                        out_invoice_obj.invoice_line_ids = [
                            (0, 0,
                             {
                                 "product_id": product_obj.id,
                                 "name": product_obj.display_name,
                                 "lot_ids": [(6, 0, lot_ids)],
                                 "quantity": 1,
                                 "price_unit": total_rent,
                                 "vehicle_licence_ids": [(6, 0, all_vehicles)],
                                 "vehicle_car_details_ids": [(6, 0, vehicle_car_details_id)],
                                 "date_from": date_from,
                                 "date_to": date_to,
                                 "total_km": total_km,
                                 "km_reading": km_reading,
                                 "extra_km": extra_km,
                                 "vo_payment_ids": [(6, 0, vo_payment_ids)],
                                 "tax_ids": [(6, 0, tax_ids)],

                             },
                             )]

                        if rec.is_grouped == True and not rec.invoice_id:
                            rec.invoice_id = out_invoice_obj.id

    def create_invoice_action_millage(self):
        for vo in self:
            if sum(vo.millage_car_details_ids.filtered(lambda x: x.is_grouped).mapped(
                    'extra_km')) < vo.limited_poolmillage_extra:
                raise ValidationError(_("Your invoice not exceeded the maximum of limited poolmillage."))

            if not vo.product_id:
                raise ValidationError('Please Select Product for Vehicle Order')
            if not vo.journal_id:
                raise ValidationError('Please Select Journal for Vehicle Order')
            if not vo.customer_id:
                raise ValidationError('Please Select Customer for Vehicle Order')
            all_vehicles_date = []
            all_payment_line = []
            total_extra_km = 0.0
            km_reading = 0.0
            for rec in vo.millage_car_details_ids:
                if rec.is_grouped == True and not rec.invoice_id:
                    all_vehicles_date.append(rec.date_from)
                    if vo.pool_millage == True:
                        total_extra_km += rec.extra_km
                        km_reading += rec.km_reading
                        all_payment_line.append(rec.id)
            if total_extra_km > vo.limited_poolmillage_extra:
                total_extra_km_pool = total_extra_km - vo.limited_poolmillage_extra
            else:
                total_extra_km_pool = total_extra_km
            set_all_vehicles = set(all_vehicles_date)
            if len(set_all_vehicles) > 1:
                raise ValidationError('Please Select lines with same Dates')

            if vo.extra_km > 0:
                print(f'in create_invoice_action_millage = vo.extra_km > 0 = vo.extra_km:{vo.extra_km} ')
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": vo.customer_id.id,
                        "journal_id": vo.journal_id.id,
                        "vo_id": vo.id,
                        "mla_id": vo.mla_id.id,
                        'invoice_date': vo.create_date,
                        "move_type": "out_invoice",
                        "invoice_line_ids": []})

            else:
                print(f'in create_invoice_action_millage = vo.extra_km <<<<< 0 = vo.extra_km:{vo.extra_km} ')
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": vo.customer_id.id,
                        "journal_id": vo.journal_id.id,
                        "vo_id": vo.id,
                        'invoice_date': vo.create_date,
                        "mla_id": vo.mla_id.id,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [],
                    })
            print(f'in create_invoice_action_millage - out_invoice_obj:{out_invoice_obj}')
            out_invoice_obj_indvidual2_flag = False
            for rec in vo.millage_car_details_ids:
                total_rent = 0.0
                total_km = 0.0
                # km_reading = 0.0
                extra_km = 0.0
                vehicle_car_details_id = []
                vehicle_licence = False
                tax_ids = []
                vo_payment_ids = []
                all_vehicles = []
                lot_ids = []

                if rec.is_grouped == True and not rec.invoice_id:
                    all_vehicles_date.append(rec.date_from)
                    if rec.vehicle_licence:
                        all_vehicles.append(rec.vehicle_licence.id)
                        if rec.vehicle_licence.lot_id:
                            lot_ids.append(rec.vehicle_licence.lot_id.id)
                    print(f'in create_invoice_action_millage - caserec.is_grouped == True and not rec.invoice_id   - all_vehicles :{all_vehicles} - lot_ids:{lot_ids}')
                    total_rent += rec.total_rent
                    vehicle_licence = rec.vehicle_licence
                    vehicle_car_details_id.append(rec.vehicle_car_details_id.id),
                    date_from = rec.date_from
                    date_to = rec.date_to
                    total_km += rec.total_km
                    # km_reading += rec.km_reading
                    extra_km += rec.extra_km
                    product_object = False
                    product_extra = self.env['product.product'].search(
                        [('extra_km', '=', True), ('detailed_type', '=', 'service')], limit=1)
                    print(f'create_invoice_action_millage - product_extra before :{product_extra} - km_reading :{km_reading}')
                    if len(product_extra) > 0:
                        product_object = product_extra
                    else:
                        print(f'in create_invoice_action_millage - no product_extra - it will be created ')
                        product_object = self.env['product.product'].create(
                            {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                        print(f'in create_invoice_action_millage - no product_extra - product_object new is :{product_object} ')

                    if rec.vat_id:
                        tax_ids.append(rec.vat_id.id)
                    vo_payment_ids.append(rec.id)
                    if vo.extra_km > 0:
                        print(f'in create_invoice_action_millage - vo extra km : {vo.extra_km}')
                        if vo.pool_millage != True:
                            print(f'in create_invoice_action_millage - vo extra km2222 : {vo.extra_km} - vo.pool_millage :{vo.pool_millage}')
                            # product_obj = self.env['product.product'].create(
                            #     {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                            out_invoice_obj.invoice_line_ids = [
                                (0, 0,
                                 {

                                     "product_id": product_object.id,
                                     "name": vo.product_id.display_name,
                                     "millage_invoice_ids": [(4, rec.id)],

                                     "vehicle_car_details_ids": [(4, rec.vehicle_car_details_id.id)],
                                     "quantity": rec.extra_km,
                                     "price_unit": rec.vehicle_id.extra_km,
                                     # "km_reading": rec.km_reading,
                                     "km_reading": km_reading,
                                     'date_from': rec.date_from,
                                     'date_to': rec.date_to,
                                     "extra_km": total_extra_km_pool,

                                 },
                                 )
                            ]

                            if rec.is_grouped == True and not rec.invoice_id:
                                rec.invoice_id = out_invoice_obj.id
                        else:
                            print(f'in create_invoice_action_millage eeeeeeeeeeeelss- case pool millage is trueee')
                            if vo.invoice_policy == 'grouped':
                                print(f'in create_invoice_action_millage = case invoice policy grouped ')
                                there_is_km = []
                                total_km = 0
                                print(f'in create_invoice_action_millage - out_invoice_obj:{out_invoice_obj} - out_invoice_obj.invoice_line_ids :{out_invoice_obj.invoice_line_ids} ')
                                for inv_line in out_invoice_obj.invoice_line_ids:

                                    if inv_line.name == 'Extra KM':
                                        print(f'in create_invoice_action_millage - there us inv_line is Extra KM  - inv_line id :{inv_line.id}')
                                        there_is_km.append(inv_line)
                                        print(f'there_is_km after appedn :{there_is_km}')
                                if not there_is_km:
                                    # product_obj = self.env['product.product'].create(
                                    #     {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                                    print(f'in create_invoice_action_millage not there_is_km - :{there_is_km} ')
                                    out_invoice_obj.invoice_line_ids = [
                                        (0, 0,
                                         {
                                             "product_id": product_object.id,
                                             "name": vo.product_id.display_name,
                                             "millage_invoice_ids": [(4, rec.id)],
                                             "vehicle_car_details_ids": [(4, rec.vehicle_car_details_id.id)],
                                             "quantity": total_extra_km_pool,
                                             "price_unit": rec.vehicle_id.extra_km,
                                             'date_from': rec.date_from,
                                             'date_to': rec.date_to,
                                             # "km_reading": rec.km_reading,
                                             "km_reading": km_reading,
                                             "extra_km": total_extra_km_pool,

                                         },
                                         )
                                    ]
                                    print(f'in create_invoice_action_millage not there_is_km - out_invoice_obj after createddd22:{out_invoice_obj} ')

                                total_expexted = 0
                                # if rec.is_grouped == True and not rec.invoice_id:
                                #     rec.invoice_id = out_invoice_obj.id
                                lines_groued = vo.millage_car_details_ids.filtered(
                                    lambda x: x.is_grouped and not x.invoice_id)
                                print(f'lines_groued11111111 :{lines_groued}')
                                license_lst = []
                                car_details = []
                                for line in lines_groued:
                                    line.invoice_id = out_invoice_obj.id
                                    total_expexted += line.total_km
                                    print(f'lines_groued11111111222 :{lines_groued} = line.invoice_id:{line.invoice_id} - total_expexted :{total_expexted}')
                                    license_lst.append(line.vehicle_licence.id)
                                    car_details.append(line.vehicle_car_details_id.id)
                                    print(f'lines_groued11111111222 :{lines_groued} = license_lst:{license_lst} - car_details :{car_details}')

                                # out_invoice_obj.invoice_line_ids.update({
                                #     'vehicle_licence_ids': license_lst,
                                #     'vehicle_car_details_ids': car_details,
                                #     'total_km': total_expexted
                                # })
                                out_invoice_obj.invoice_line_ids.write({
                                    'vehicle_licence_ids': license_lst,
                                    'vehicle_car_details_ids': car_details,
                                    'total_km': total_expexted,
                                    "extra_km": total_extra_km_pool,
                                    "km_reading": km_reading,

                                })

                                print(
                                    f'lines_groued11111111222333 :{lines_groued} = vehicle_licence_ids - out_invoice_obj.invoice_line_ids :{out_invoice_obj.invoice_line_ids}- license_lst :{license_lst} - vehicle_car_details_ids car_details :{car_details} - total_km total_expexted:{total_expexted} - km_reading :{km_reading}')

                                break
                            else:
                                print(f'in create_invoice_action_millage = case  not ttttttt invoice policy grouped ')
                                there_is_km = []
                                for inv_line in out_invoice_obj.invoice_line_ids:
                                    if inv_line.name == 'Extra KM':
                                        there_is_km.append(inv_line)
                                        print(
                                        f'in create_invoice_action_millage = case  not ttttttt22 invoice policy grouped = case extra lkmmmmmm2222  - inv_line.name:{inv_line.name} ')

                                if not there_is_km:
                                    print(
                                        f'in create_invoice_action_millage = case  not ttttttt2332 invoice policy grouped = case extra lkmmmmmm2222  - not there_is_km: {there_is_km} ')
                                    # product_obj = self.env['product.product'].create(
                                    #     {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})

                                    if not out_invoice_obj_indvidual2_flag:
                                        print(
                                            f'in create_invoice_action_millage = case not out_invoice_obj_indvidual2_flag')
                                        out_invoice_obj_indvidual2 = self.env["account.move"].create(
                                            {
                                                "partner_id": vo.customer_id.id,
                                                "journal_id": vo.journal_id.id,
                                                "vo_id": vo.id,
                                                "mla_id": vo.mla_id.id,
                                                'invoice_date': vo.create_date,
                                                "move_type": "out_invoice",
                                                "invoice_line_ids": [(0, 0,
                                                                      {
                                                                          "product_id": product_object.id,
                                                                          "name": vo.product_id.display_name,
                                                                          "vehicle_licence_ids": vehicle_licence,
                                                                          "quantity": total_extra_km_pool,
                                                                          "price_unit": rec.vehicle_id.extra_km,
                                                                          "millage_invoice_ids": [(4, rec.id)],
                                                                          # "km_reading": rec.km_reading,
                                                                          "km_reading": km_reading,
                                                                          'date_from': rec.date_from,
                                                                          'date_to': rec.date_to,
                                                                          "extra_km": total_extra_km_pool,

                                                                      },
                                                                      ), ]})
                                        print(
                                            f'in create_invoice_action_millage = case not out_invoice_obj_indvidual2_flag - out_invoice_obj_indvidual2  after creaaaated:{out_invoice_obj_indvidual2}')
                                        out_invoice_obj_indvidual2_flag = out_invoice_obj_indvidual2
                                        vo.extra_km_invoice_ids = [(4, out_invoice_obj_indvidual2.id)]


class VehicleOrderPayment(models.Model):
    _inherit = 'vehicle.order.payment'
    no_of_days = fields.Integer(compute='clc_no_of_days')
    total_rent = fields.Float(string="Total Monthly Rent", required=False, compute='clc_monthly_rent', readonly=0)

    @api.depends('no_of_days')
    def clc_monthly_rent(self):
        for rec in self:

            start_dt = fields.Datetime.from_string(rec.date_from)
            finish_dt = fields.Datetime.from_string(rec.date_to + relativedelta(days=1))
            difference = relativedelta(finish_dt, start_dt)
            if rec.vehicle_id.unit_price > 0 and difference.months < rec.vehicle_id.invoice_every_months:
                rec.total_rent = (rec.vehicle_id.unit_price / 30) * rec.no_of_days

            elif rec.vehicle_id.unit_price > 0 and difference.months > 0:
                rec.total_rent = rec.vehicle_id.unit_price * rec.vehicle_id.invoice_every_months

            else:
                rec.total_rent = 0

    def clc_no_of_days(self):
        for rec in self:
            rec.no_of_days = 0
            if rec.date_to and rec.date_from:
                rec.no_of_days = (rec.date_to - rec.date_from).days

    def create_invoice_action(self):
        for rec in self:
            if not rec.vehicle_id.product_id:
                raise ValidationError('Please Select Product for Vehicle Order')
            if not rec.vehicle_id.journal_id:
                raise ValidationError('Please Select Journal for Vehicle Order')
            if not rec.vehicle_id.customer_id:
                raise ValidationError('Please Select Customer for Vehicle Order')

            vat_id = []
            if rec.vat_id:
                vat_id.append((4, rec.vat_id.id))

            lot_id = []
            vehicle_licence = []
            product_object = False
            if rec.vehicle_licence:
                vehicle_licence.append((4, rec.vehicle_licence.id))
                if rec.vehicle_licence.lot_id:
                    lot_id.append((4, rec.vehicle_licence.lot_id.id))
            if rec.vehicle_id.extra_km > 0:

                # product_obj = self.env['product.product'].create(
                #     {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                # product_extra = self.env['product.product'].search(
                #     [('extra_km', '=', True), ('detailed_type', '=', 'service')], limit=1)
                # if len(product_extra) > 0:
                #     product_object = product_extra
                # else:
                #     product_obj = self.env['product.product'].create(
                #             {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": rec.vehicle_id.customer_id.id,
                        "journal_id": rec.vehicle_id.journal_id.id,
                        "vo_id": rec.vehicle_id.id,
                        "mla_id": rec.vehicle_id.mla_id.id,
                        'invoice_date': rec.create_date,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [
                            (0, 0,
                             {
                                 "product_id": rec.vehicle_id.product_id.id,
                                 "name": rec.vehicle_id.product_id.display_name,
                                 "lot_ids": lot_id,
                                 "quantity": 1,
                                 "price_unit": rec.total_rent,
                                 "vehicle_licence_ids": vehicle_licence,
                                 "vehicle_car_details_ids": [(4, rec.vehicle_car_details_id.id)],
                                 "date_from": rec.date_from,
                                 "date_to": rec.date_to,
                                 "total_km": rec.total_km,
                                 "km_reading": rec.km_reading,
                                 "extra_km": rec.extra_km,
                                 "vo_payment_ids": [(4, rec.id)],
                                 "tax_ids": vat_id,
                             },
                             ),
                        ],
                    })
                rec.invoice_id = out_invoice_obj
            else:
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": rec.vehicle_id.customer_id.id,
                        "journal_id": rec.vehicle_id.journal_id.id,
                        "vo_id": rec.vehicle_id.id,
                        'invoice_date': rec.create_date,
                        "mla_id": rec.vehicle_id.mla_id.id,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [
                            (0, 0,
                             {
                                 "product_id": rec.vehicle_id.product_id.id,
                                 "name": rec.vehicle_id.product_id.display_name,
                                 "lot_ids": lot_id,
                                 "quantity": 1,
                                 "price_unit": rec.total_rent,
                                 "vehicle_licence_ids": vehicle_licence,
                                 "vehicle_car_details_ids": [(4, rec.vehicle_car_details_id.id)],
                                 "date_from": rec.date_from,
                                 "date_to": rec.date_to,
                                 "total_km": rec.total_km,
                                 "km_reading": rec.km_reading,
                                 "extra_km": rec.extra_km,
                                 "vo_payment_ids": [(4, rec.id)],
                                 "tax_ids": vat_id,

                             },
                             )
                        ],
                    })
                rec.invoice_id = out_invoice_obj
