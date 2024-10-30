# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.addons.fleet.models.fleet_vehicle_model import FUEL_TYPES


class VehicleOrder(models.Model):
    _inherit = 'vehicle.order'

    limited_monthly_km = fields.Float(string="Limited Monthly KM", compute="compute_limited_monthly_km")
    limited_poolmillage = fields.Float(string="Limited Pool Millage", compute="compute_limited_pool_millage_km")
    extra_km_invoice_ids = fields.Many2many("account.move", string='Invoices', copy=False)

    @api.depends('km_year')
    def compute_limited_monthly_km(self):
        for rec in self:
            if rec.km_year > 0:
                rec.limited_monthly_km = rec.km_year / 12
            else:
                rec.limited_monthly_km = 0.0
    @api.depends('km_year', 'invoice_every_months', 'no_Vehicles')
    def compute_limited_pool_millage_km(self):
        for rec in self:
            if rec.km_year > 0:
                rec.limited_poolmillage = (rec.km_year / 12) * rec.invoice_every_months * rec.no_Vehicles
            else:
                rec.limited_poolmillage = 0.0

    def update_odometer_value(self):
        for rec in self:
            for line in rec.vehicle_car_ids:
                odometer_obj = self.env['fleet.vehicle.odometer'].search(
                    [('vehicle_id', '=', line.fleet_licence_plate_id.id)], order='date desc , value desc', limit=1)
                line.total_km = odometer_obj.value

            for pay in rec.vehicle_payments:
                # odometer_date_to_obj = self.env['fleet.vehicle.odometer'].search(
                #     [('date', '<=', pay.date_to), ('vehicle_id', '=', pay.vehicle_licence.id), ('vo_id', '=',rec.id)], order='date desc')
                # odometer_date_from_obj = self.env['fleet.vehicle.odometer'].search(
                #     [('date', '>=', pay.date_from), ('date', '<', pay.date_to), ('vo_id', '=',rec.id),
                #      ('vehicle_id', '=', pay.vehicle_licence.id)], order='date asc')
                # total_date_to_val = 0.0
                # total_date_from_val = 0.0
                # for odo_to_val in odometer_date_to_obj:
                #     total_date_to_val += odo_to_val.value
                #     break
                # for odo_from_val in odometer_date_from_obj:
                #     total_date_from_val += odo_from_val.value
                #     break
                # pay.km_reading = total_date_to_val - total_date_from_val
                odometer = self.env['fleet.vehicle.odometer'].search([
                    ('date', '>=', pay.date_from), ('date', '<=', pay.date_to),
                    ('vehicle_id', '=', pay.vehicle_licence.id),
                    ('vo_id', '=', rec.id)
                ], order='date desc', limit=1)
                if odometer:
                   pay.km_reading = odometer.value
                else:
                    pay.km_reading = 0.0
                # extra_km = pay.km_reading - rec.limited_monthly_km
                extra_km = pay.km_reading - pay.total_km
                if extra_km > 0:
                    pay.extra_km = extra_km
                else:
                    pay.extra_km = 0.0
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
            if total_extra_km > vo.limited_poolmillage:
                total_extra_km_pool = total_extra_km - vo.limited_poolmillage
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
                        # 'invoice_date': vo.create_date,
                        'invoice_date': fields.Date.today(),
                        "move_type": "out_invoice",
                        "invoice_line_ids": []})

            else:
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": vo.customer_id.id,
                        "journal_id": vo.journal_id.id,
                        "vo_id": vo.id,
                        # 'invoice_date': vo.create_date,
                        'invoice_date': fields.Date.today(),
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
                    vehicle_car_details_id.append(rec.vehicle_car_details_id.id),
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
                            product_obj = self.env['product.product'].create(
                                {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                            out_invoice_obj.invoice_line_ids = [
                                        (0, 0,
                                         {
                                             "product_id": vo.product_id.id,
                                             "name": vo.product_id.display_name,
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
                                         ), (0, 0,
                                             {
                                                 "product_id": product_obj.id,
                                                 "name": product_obj.display_name,
                                                 "quantity": rec.extra_km,
                                                 "price_unit": rec.vehicle_id.extra_km,
                                                 # "vehicle_licence": rec.vehicle_licence.id,
                                                 # "vehicle_car_details_id": rec.vehicle_car_details_id.id,
                                                 # "date_from": rec.date_from,
                                                 # "date_to": rec.date_to,
                                                 # "total_km": rec.total_km,
                                                 "vo_payment_ids": [(4, rec.id)],
                                             },
                                             )
                                    ]

                            if rec.is_grouped == True and not rec.invoice_id:
                                rec.invoice_id = out_invoice_obj.id
                        else:
                            if vo.invoice_policy == 'grouped':
                                there_is_km=[]
                                for inv_line in out_invoice_obj.invoice_line_ids:
                                    if inv_line.name == 'Extra KM':
                                        there_is_km.append(inv_line)
                                if not there_is_km:
                                    product_obj = self.env['product.product'].create(
                                        {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                                    out_invoice_obj.invoice_line_ids = [
                                    (0, 0,
                                     {
                                         "product_id": vo.product_id.id,
                                         "name": vo.product_id.display_name,
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
                                     ), (0, 0,
                                         {
                                             "product_id": product_obj.id,
                                             "name": product_obj.display_name,
                                             "quantity": total_extra_km_pool,
                                             "price_unit": rec.vehicle_id.extra_km,
                                             # "vehicle_licence": rec.vehicle_licence.id,
                                             # "vehicle_car_details_id": rec.vehicle_car_details_id.id,
                                             # "date_from": rec.date_from,
                                             # "date_to": rec.date_to,
                                             # "total_km": rec.total_km,
                                             "vo_payment_ids": [(6,0, all_payment_line)],
                                         },
                                         )
                                ]
                                else:
                                    out_invoice_obj.invoice_line_ids = [
                                        (0, 0,
                                         {
                                             "product_id": vo.product_id.id,
                                             "name": vo.product_id.display_name,
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
                                    product_obj = self.env['product.product'].create(
                                        {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})
                                    out_invoice_obj_indvidual = self.env["account.move"].create(
                                        {
                                            "partner_id": vo.customer_id.id,
                                            "journal_id": vo.journal_id.id,
                                            "vo_id": vo.id,
                                            "mla_id": vo.mla_id.id,
                                            # 'invoice_date': vo.create_date,
                                            'invoice_date': fields.Date.today(),
                                            "move_type": "out_invoice",
                                            "invoice_line_ids": [(0, 0,
                                         {
                                             "product_id": vo.product_id.id,
                                             "name": vo.product_id.display_name,
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
                                         ),]})
                                    if not out_invoice_obj_indvidual2_flag:
                                        out_invoice_obj_indvidual2 = self.env["account.move"].create(
                                            {
                                                "partner_id": vo.customer_id.id,
                                                "journal_id": vo.journal_id.id,
                                                "vo_id": vo.id,
                                                "mla_id": vo.mla_id.id,
                                                # 'invoice_date': vo.create_date,
                                                'invoice_date': fields.Date.today(),
                                                "move_type": "out_invoice",
                                                "invoice_line_ids": [(0, 0,
                                                 {
                                                     "product_id": product_obj.id,
                                                     "name": product_obj.display_name,
                                                     "quantity": total_extra_km_pool,
                                                     "price_unit": rec.vehicle_id.extra_km,
                                                     # "vehicle_licence": rec.vehicle_licence.id,
                                                     # "vehicle_car_details_id": rec.vehicle_car_details_id.id,
                                                     # "date_from": rec.date_from,
                                                     # "date_to": rec.date_to,
                                                     # "total_km": rec.total_km,
                                                     "vo_payment_ids": [(6, 0, all_payment_line)],
                                                 },
                                                 ),]})
                                        out_invoice_obj_indvidual2_flag = out_invoice_obj_indvidual2
                                        vo.extra_km_invoice_ids = [(4,out_invoice_obj_indvidual2.id)]

                                else:
                                    out_invoice_obj_indvidual = self.env["account.move"].create(
                                        {
                                            "partner_id": vo.customer_id.id,
                                            "journal_id": vo.journal_id.id,
                                            "vo_id": vo.id,
                                            "mla_id": vo.mla_id.id,
                                            # 'invoice_date': vo.create_date,
                                            'invoice_date': fields.Date.today(),
                                            "move_type": "out_invoice",
                                            "invoice_line_ids": [   (0, 0,
                                         {
                                             "product_id": vo.product_id.id,
                                             "name": vo.product_id.display_name,
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
                                         ), ]})


                                if rec.is_grouped == True and not rec.invoice_id:
                                    rec.invoice_id =  out_invoice_obj_indvidual.id

                    else:
                        out_invoice_obj.invoice_line_ids = [
                                    (0, 0,
                                     {
                                         "product_id": vo.product_id.id,
                                         "name": vo.product_id.display_name,
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



class VehicleOrderPayment(models.Model):
    _inherit = 'vehicle.order.payment'

    km_reading = fields.Float(string="Consumed KM")
    extra_km = fields.Float(string="Extra KM")

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
                vat_id.append((4,rec.vat_id.id))

            lot_id = []
            vehicle_licence = []
            if rec.vehicle_licence:
                vehicle_licence.append((4,rec.vehicle_licence.id))
                if rec.vehicle_licence.lot_id:
                    lot_id.append((4,rec.vehicle_licence.lot_id.id))
            if rec.vehicle_id.extra_km > 0:
                product_obj = self.env['product.product'].create(
                    {'name': 'Extra KM', 'extra_km': True, 'detailed_type': 'service'})

                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": rec.vehicle_id.customer_id.id,
                        "journal_id": rec.vehicle_id.journal_id.id,
                        "vo_id": rec.vehicle_id.id,
                        "mla_id": rec.vehicle_id.mla_id.id,
                        # 'invoice_date': rec.create_date,
                        'invoice_date': fields.Date.today(),
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
                             ), (0, 0,
                                 {
                                     "product_id": product_obj.id,
                                     "name": product_obj.display_name,
                                     "quantity": rec.extra_km,
                                     "price_unit": rec.vehicle_id.extra_km,
                                     # "vehicle_licence": rec.vehicle_licence.id,
                                     # "vehicle_car_details_id": rec.vehicle_car_details_id.id,
                                     # "date_from": rec.date_from,
                                     # "date_to": rec.date_to,
                                     # "total_km": rec.total_km,
                                     "vo_payment_ids": [(4, rec.id)],
                                 },
                                 )
                        ],
                    })
                rec.invoice_id = out_invoice_obj
            else:
                out_invoice_obj = self.env["account.move"].create(
                    {
                        "partner_id": rec.vehicle_id.customer_id.id,
                        "journal_id": rec.vehicle_id.journal_id.id,
                        "vo_id": rec.vehicle_id.id,
                        # 'invoice_date': rec.create_date,
                        'invoice_date': fields.Date.today(),
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
