# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    vo_id = fields.Many2one("vehicle.order", string='Serial Vehicle Order')
    mla_id = fields.Many2one(comodel_name="mla.data", string="Serial MLA")
    # vehicle_car_details_ids = fields.Many2many("vehicle.car.details", string="Car Details Seq")
    # fleet_vehicle_ids = fields.Many2one("fleet.vehicle", string="Vehicles License Plate",compute='get_vehicle_licence',store=True)
    # fleet_vehicle_license_plate = fields.Char(string="Vehicles License Plate",compute='get_vehicle_license_plate',store=True)
    invoices_date_from = fields.Date("Invoices Date From",compute='get_invoices_date_from',store=True)
    invoices_date_to = fields.Date("Invoices Date To",compute='get_invoices_date_to',store=True)

    # @api.depends('fleet_vehicle_ids')
    # def get_vehicle_license_plate(self):
    #     print(f'in get_vehicle_license_plate')
    #     for rec in self:
    #         if rec.fleet_vehicle_ids :
    #             rec.fleet_vehicle_license_plate = rec.fleet_vehicle_ids.license_plate
    #         else:
    #             rec.fleet_vehicle_license_plate = None
    #
    # @api.depends('invoice_line_ids')
    # def get_vehicle_licence(self):
    #     print(f'in get_vehicle_licence')
    #     fleet_vehicle_id = None
    #     for rec in self:
    #         if rec.invoice_line_ids:
    #             if rec.invoice_line_ids[0].vehicle_licence_ids:
    #                 fleet_vehicle_id = rec.invoice_line_ids[0].vehicle_licence_ids[0]
    #         rec.fleet_vehicle_ids = fleet_vehicle_id

    @api.depends('invoice_line_ids')
    def get_invoices_date_from(self):
        print(f'in get_invoices_date_from')
        for rec in self:
            if rec.invoice_line_ids:
                rec.invoices_date_from = rec.invoice_line_ids[0].date_from
            else:
                rec.invoices_date_from = False

    @api.depends('invoice_line_ids')
    def get_invoices_date_to(self):
        print(f'in get_invoices_date_to')
        # invoices_date_to_list = []
        for rec in self:
            if rec.invoice_line_ids:
                rec.invoices_date_to = rec.invoice_line_ids[0].date_to
            else:
                rec.invoices_date_to = False

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    vehicle_licence = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle License Plate", required=False, )
    vehicle_licence_ids = fields.Many2many("fleet.vehicle",'vo_fleet_col1','vo_fleet_col2','vo_fleet_rel', string="Vehicle License Plate", required=False, )
    lot_ids = fields.Many2many('stock.production.lot', string="Lot/Serial")
    vehicle_car_details_ids = fields.Many2many("vehicle.car.details", string="Car Details Seq")
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    total_km = fields.Float(string="Expected Total KM")
    vo_payment_id = fields.Many2one("vehicle.order.payment", string='VO')
    vo_payment_ids = fields.Many2many("vehicle.order.payment",'vo_payment_col1','vo_payment_col2','vo_payment_rel', string='VO')
    km_reading = fields.Float(string="Consumed KM")
    extra_km = fields.Float(string="Extra KM")



