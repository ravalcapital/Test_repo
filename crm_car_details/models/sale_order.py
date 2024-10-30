# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    crm_id = fields.Many2one('crm.lead', string='Crm')
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers")
    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models", )
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Model Category")
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year")
    color_ids = fields.Many2many("crm.car.color", string="Colors")
    car_availability = fields.Selection([('true', 'True'), ('false', 'False')],
                                        string='Car Availability')
    so_delivery_date = fields.Date("Delivery Date", default=datetime.today())
    delivery_date = fields.Datetime("Delivery Date", default=datetime.today())
    duration_in_month = fields.Integer('Duration In Month')
    millage = fields.Integer(string='Yearly Limited Allowed Per Year')
    percentage = fields.Integer(string="Percentage (%)")
    max_daily_km = fields.Float('Minimum Daily KM', default=120)
    license_plate = fields.Many2one('fleet.vehicle', string="License Plate")
    purchasing_value = fields.Float('Purchasing Value')
    extra_km = fields.Float('Extra KM')
    order_line_km_per_year = fields.Integer('KM/Year')

    @api.onchange('make_m_id')
    def onchange_make_m_id(self):
        print(f' in on change make_m_id - self :{self} - self.make_m_id:{self.make_m_id}')
        fleet_manufacturers_obj = self.env['fleet.vehicle.model.brand'].browse(self.make_m_id.id)
        List_fleet_manufacturers = []
        res = {}
        for rec in self:
            if rec.make_m_id:
                if rec.make_m_id.model_ids:
                    for model in rec.make_m_id.model_ids:
                        List_fleet_manufacturers.append(model.id)
                    res = {}
                    res['domain'] = {
                        'model_m_id': [('id', 'in', List_fleet_manufacturers)],
                    }
                    return res
                else:
                    res={}
                    List_fleet_manufacturers=[]
                    res['domain'] = {
                        'model_m_id': [('id', 'in', List_fleet_manufacturers)],
                    }
                    # res['domain'] = {
                    #     'model_m_id': [],
                    # }
                    print(f'in onchange_make_m_id -no modelsssw retuurn res:{res}')
                    return res