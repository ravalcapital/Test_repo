# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    crm_car_ids = fields.One2many('crm.car.details', 'crm_id', string="Car Details")
    option_to_puy = fields.Selection([('lease_to_own', 'Lease to Own'), ('operating_lease', 'Operating Lease')],
                                     string='Leasing Type')

    contract_term = fields.Selection([('long_term', 'Long Term'), ('short_term', 'Short Term')],
                                     string='Contract Term')
    millage_calculation = fields.Selection([('pool', 'Pool'), ('limited_km', 'Limited KM')],
                                           string='Millage Calculation')
    total_pool_millage = fields.Float(string='Total Pool Millage')
    decision_id = fields.Many2one('res.partner', domain="[('id','in',decision_ids)]", string="Decision Maker")
    decision_ids = fields.Many2many('res.partner', 'par_relation', 'att1', 'att2', compute='child_ids')
    mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", required=False, )
    start_date = fields.Date("Start Date", related="mla_id.start_date", store=True)
    end_date = fields.Date("End Date", related="mla_id.end_date", store=True)
    vo_ids = fields.One2many("vehicle.order", 'crm_id', string="VO")

    @api.depends('partner_id')
    def child_ids(self):
        child = []
        for l in self:
            if l.partner_id:
                for rec in l.partner_id.child_ids:
                    print(rec)
                    child.append(rec.id)
                if child:
                    l.decision_ids = child
                else:
                    l.decision_ids = False
            else:
                l.decision_ids = False

    @api.constrains('contract_term', 'crm_car_ids', 'crm_car_ids.duration_in_month')
    def _check_contract_term(self):
        if self.contract_term == 'short_term':
            contract_list_term = []
            for line in self.crm_car_ids:
                if line.duration_in_month > 12:
                    contract_list_term.append(line)
            if len(contract_list_term) > 0:
                raise ValidationError("Duration in months in car details should not exceed 12")

    @api.onchange('partner_id')
    def _onchange_partner_vo(self):
        all_vo = []
        for rec in self:
            if rec.partner_id:
                vehicle_order = self.env['vehicle.order']
                vehicle_order_ids = vehicle_order.search([('customer_id', '=', rec.partner_id.id)])
                for line in vehicle_order_ids:
                    all_vo.append(line.id)
                rec.vo_ids = [(6, 0, all_vo)]

    @api.constrains('millage_calculation', 'crm_car_ids.', 'crm_car_ids.category_m_id', 'crm_car_ids.make_m_id',
                    'crm_car_ids.year_id',
                    'crm_car_ids.model_m_id')
    def _check_crm_car_ids_lines(self):
        category_m = []
        make_m = []
        model_m = []
        year_m = []
        for line in self.crm_car_ids:
            category_m.append(line.category_m_id.id)
            make_m.append(line.make_m_id.id)
            model_m.append(line.model_m_id.id)
            year_m.append(line.year_id.id)
        if len(set(category_m)) > 1 and self.millage_calculation == 'pool':
            raise ValidationError("All Car Details lines should have the same Model Category")
        if len(set(make_m)) > 1 and self.millage_calculation == 'pool':
            raise ValidationError("All Car Details lines should have the same Manufactures")
        if len(set(model_m)) > 1 and self.millage_calculation == 'pool':
            raise ValidationError("All Car Details lines should have the same Vehicle Model")
        if len(set(year_m)) > 1 and self.millage_calculation == 'pool':
            raise ValidationError("All Car Details lines should have the same Year")

    def action_new_quotation(self):
        action = super().action_new_quotation()
        all_lines = []
        for line in self.crm_car_ids:
            vals = {'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'product_uom': line.product_id.uom_id.id,
                    'make_m_id': line.make_m_id.id,
                    'model_m_id': line.model_m_id.id,
                    'category_m_id': line.category_m_id.id,
                    'year_id': line.year_id.id,
                    'color_ids': [(6, 0, line.color_ids.ids)],
                    'product_uom_qty': line.qty,
                    'car_availability': line.car_availability,
                    'so_delivery_date': line.delivery_date,
                    'price_unit': line.list_price,
                    'duration_in_month': line.duration_in_month,
                    'millage': line.millage,
                    'license_plate': line.license_plate.id,
                    'purchasing_value': line.purchasing_value,
                    }
            all_lines.append((0, 0, vals))
        action['context']['default_order_line'] = all_lines
        return action


class CrmCarDetails(models.Model):
    _name = 'crm.car.details'
    _description = 'Car Details'

    crm_id = fields.Many2one('crm.lead', string='Crm')
    contract_term = fields.Selection([('long_term', 'Long Term'), ('short_term', 'Short Term')],
                                     string='Contract Term',related='crm_id.contract_term')
    product_id = fields.Many2one('product.product', string='Car', required=True, domain=[('is_vehicle', '=', True)])
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers")
    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models")
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Model Category")
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year")
    color_ids = fields.Many2many("crm.car.color", string="Colors")
    qty = fields.Integer('QTY')
    car_availability = fields.Selection([('true', 'True'), ('false', 'False')],
                                        string='Car Availability')
    delivery_date = fields.Date("Delivery Date", default=lambda self: fields.Datetime.now())
    # list_price = fields.Float('Purchasing Value')
    list_price = fields.Float('Monthly Rent')
    purchasing_value = fields.Float('Purchasing Value')
    duration_in_month = fields.Integer('Months')
    millage = fields.Integer(string='Yearly Allowed')
    percentage = fields.Integer(string="Percentage (%)")
    max_daily_km = fields.Float(' Maximum Daily KM', default=120)
    # license_plate = fields.Many2one('fleet.vehicle',string="License Plate",)
    def get_license_plate_domain(self):
        domain = []
        short_car_identity = self.env['car.identity'].search([('name', '=', 'Short Term')], limit=1)
        if short_car_identity:
            car_identity_short_term = self.env['fleet.vehicle'].search(
                [('car_identity_id', '=', short_car_identity.id)])
            if car_identity_short_term:
                domain = [('id', 'in', car_identity_short_term.ids)]
        return domain
    license_plate = fields.Many2one('fleet.vehicle', string="License Plate", domain=get_license_plate_domain)

    @api.onchange('contract_term','license_plate')
    def _onchange_contract_term_license_plate(self):
        for rec in self:
            if rec.contract_term =='short_term':
                if rec.license_plate:
                    rec.model_m_id = rec.license_plate.model_id.id
                    rec.make_m_id = rec.license_plate.model_id.brand_id.id
                    rec.year_id = rec.license_plate.year_id.id
            else:
                rec.license_plate= False
                rec.model_m_id = False
                rec.make_m_id = False
                rec.year_id = False


    @api.constrains('max_daily_km')
    def _check_max_daily_km(self):
        for rec in self:
            if rec.max_daily_km < 120:
                raise ValidationError("Minimum Daily KM should not less than 120")


class VehicleOrder(models.Model):
    _inherit = 'vehicle.order'

    crm_id = fields.Many2one('crm.lead', string='Crm')
