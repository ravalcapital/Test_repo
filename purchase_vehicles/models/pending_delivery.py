# -*- encoding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, exceptions, _, tools, SUPERUSER_ID
import datetime
from dateutil.relativedelta import relativedelta


class PendingDelivery(models.Model):
    _name = 'pending.delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Pending Delivery'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(string="Pending Delivery", required=True,
                       default="New", copy=False,
                       tracking=True, readonly=1)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('bank_papers', 'Bank'),
        ('registration', 'Registration'),
        ('policy', 'Policy'),
        ('insurance', 'Insurance'),
        ('licence', 'Licence'),
        ('done', 'Done')], string='Status',
        copy=False, default='draft', required=True, tracking=True)

    user_id = fields.Many2one('res.users', string="Responsible", domain="[('share', '=', False)]",
                              default=lambda self: self.env.user, tracking=True)
    date = fields.Datetime("Date", tracking=True, default=lambda self: fields.Datetime.now())
    notes = fields.Text("Notes", tracking=True)
    company_id = fields.Many2one('res.company', 'Company', index=True,
                                 default=lambda self: self.env.company, readonly=True, tracking=True)

    purchase_id = fields.Many2one('purchase.order', string='PO', required=True,
                                  domain="[('state', 'in', ['draft','sent','purchase','done'])]", tracking=True)
    purchase_line_id = fields.Many2one('purchase.order.line', string='PO Line', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Customer", check_company=True, index=True, tracking=10,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    receive_ids = fields.Many2many('stock.picking', string='Receive ID', compute="get_purchase_picking")
    receive_id = fields.Many2one('stock.picking', string='Receive ID', copy=False)
    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models", required=1,
                                 related="purchase_line_id.model_m_id",
                                 store=True)
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers",
                                related="purchase_line_id.make_m_id", store=True)
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Category",
                                    related="purchase_line_id.category_m_id", store=True)

    color = fields.Integer('Color Index', tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer(string="Sequence")
    vehicle_name = fields.Many2one("fleet.vehicle", string="Vehicle Name", tracking=True)
    vehicle_price = fields.Float('Vehicle Price [Excl.Tax]', related="purchase_line_id.price_unit")
    vehicle_price_incl = fields.Float('Tax', compute="compute_vehicle_price_incl")
    car_po_price = fields.Float('Car Po Price', compute="compute_car_po_price")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle ID", tracking=True, copy=False)
    vehicle_insurance_id = fields.Many2one("vehicle.insurance", string="Vehicle Insurance", tracking=True, copy=False)
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year", related="purchase_line_id.year_id", store=True)

    bank_state = fields.Selection([
        ('full_bank_installment', 'Full Bank Installment'),
        ('partial_bank_installment', 'Partial Bank Payment'), ]
        , string='bank_state',
        copy=False, tracking=True)
    bank_loan_amount = fields.Float('Bank Loan amount', tracking=True)
    bank_id = fields.Many2one('res.bank', string="Bank", tracking=True)
    bank_account_id = fields.Many2one('res.partner.bank', string="Bank Account", tracking=True)

    car_registration_number = fields.Integer('Car RegistrationNumber')
    car_engin_number = fields.Char('Car Engine number', tracking=True)
    chassis_number = fields.Char('Chassis Number', tracking=True)
    car_plate_no = fields.Char('Car Plate No.', tracking=True)
    license_year = fields.Integer('License Years', tracking=True, default=1)
    license_start_date = fields.Date('License Start date', tracking=True)
    license_renewal_date = fields.Date('License Renewal Date', compute="_compute_license_renewal_date", store=True)
    license_probation_period = fields.Date('License Probation Period', compute="_compute_license_probation_period",
                                           store=True)
    license_code = fields.Char('License Code')

    # insurance_no = fields.Integer('Insurance No.', tracking=True)
    insurance_no = fields.Char('Insurance No.', tracking=True)
    insurance_year = fields.Integer('Insurance Years', tracking=True, default=1)
    insurance_start_date = fields.Date('Insurance start date', tracking=True)
    insurance_end_date = fields.Date('Insurance Renewal Date', compute="_compute_insurance_end_date", store=True)

    vin_date = fields.Date('VIN Date', tracking=True)
    supplier_delivery_date = fields.Date('Supplier Delivery Date', tracking=True)
    vehicle_document_date = fields.Date('Vehicle Document Date', tracking=True)
    bank_po_date = fields.Date('Bank PO Date', tracking=True)
    fund_contract_sign_date = fields.Date('Fund Contract Sign Date', tracking=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    color_id = fields.Many2one('crm.car.color')

    @api.onchange("purchase_id")
    def _onchange_purchase_id(self):
        states = ["draft", "sent", "purchase", "done"]
        if self.purchase_id:
            domain = [
                ("order_id", "=", self.purchase_id.id),
                ("state", "in", states), ]

            order_lines = self.env["purchase.order.line"].search(domain, limit=1)
            self.purchase_line_id = order_lines.id

    @api.depends('license_start_date', 'license_year')
    def _compute_license_renewal_date(self):
        for record in self:
            if record.license_start_date and record.license_year:
                record.license_renewal_date = record.license_start_date + datetime.timedelta(
                    days=(record.license_year * 365))
            else:
                record.license_renewal_date = record.license_start_date

    @api.depends('license_start_date')
    def _compute_license_probation_period(self):
        for record in self:
            if record.license_start_date:
                record.license_probation_period = record.license_start_date + relativedelta(months=3)
            else:
                record.license_probation_period = record.license_start_date

    @api.depends('insurance_start_date', 'insurance_year')
    def _compute_insurance_end_date(self):
        for record in self:
            if record.insurance_start_date and record.insurance_year:
                record.insurance_end_date = record.insurance_start_date + datetime.timedelta(
                    days=(record.insurance_year * 365))
            else:
                record.insurance_end_date = record.insurance_start_date

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pending.delivery') or '/'
        return super(PendingDelivery, self).create(vals)

    @api.onchange('bank_state')
    def onchange_bank_state(self):
        for rec in self:
            if rec.bank_state == "full_bank_installment":
                rec.bank_loan_amount = self.car_po_price
            else:
                rec.bank_loan_amount = 0.0

    def action_create_vehicle(self):
        if self.state == 'done':
            self.vehicle_id = self.env['fleet.vehicle'].create({'name': self.name,
                                                                'model_id': self.model_m_id.id,
                                                                'product_id': self.purchase_line_id.product_id.id,
                                                                'net_car_value': self.vehicle_price,
                                                                'car_value': self.vehicle_price_incl,
                                                                'pending_delivery_id': self.id,
                                                                'purchase_line_id': self.purchase_line_id.id,
                                                                'year_id': self.year_id.id,
                                                                'vin_sn': self.chassis_number,
                                                                'engine_number': self.car_engin_number,
                                                                'receive_ids': [(6, 0, self.receive_ids.ids)],
                                                                }).id

    def action_create_insurance(self):
        if not self.vehicle_id:
            raise ValidationError(_('Please Create Vehicle First..!'))

        if self.state == 'done':
            self.vehicle_insurance_id = self.env['vehicle.insurance'].create({
                'model_m_id': self.model_m_id.id,
                'make_m_id': self.make_m_id.id,
                'category_m_id': self.category_m_id.id,
                'year_id': self.year_id.id,
                'from_pending_delivery': True,
                'vehicle_id': self.vehicle_id.id,
                'license_plate': self.car_plate_no,
                'date_from': self.insurance_start_date,
                'date_to': self.insurance_end_date,
                'insurance_no': self.insurance_no,
                'insurance_year': self.insurance_year,
                'pending_delivery_id': self.id,

            }).id

    def action_create_stock_move(self):
        if not self.vehicle_id:
            raise ValidationError(_('Please Create Vehicle First..!'))

        if self.state == 'done':
            if self.receive_ids:
                for receive in self.receive_ids:
                    if receive.state != 'done':
                        for rec in receive.move_ids_without_package:
                            if rec.product_id == self.purchase_line_id.product_id:
                                serial_obj = self.env['stock.production.lot']._get_next_serial(rec.company_id,
                                                                                               rec.product_id)
                                if serial_obj:
                                    serial_2 = serial_obj
                                else:
                                    serial_2 = self.env['ir.sequence'].next_by_code('stock.lot.serial')
                                lot_obj = self.env['stock.production.lot'].create(
                                    {'name': self.car_plate_no or '' + '/' + str(serial_2)
                                        ,
                                     'product_id': rec.product_id.id,
                                     'company_id': rec.company_id.id,
                                     # 'product_qty': rec.product_uom_qty,
                                     'vehicle_id': self.vehicle_id.id, })
                                rec.lot_ids = [(4, lot_obj.id)]
                                rec.picking_id.pending_delivery_id = self.id
                                rec._action_done(cancel_backorder=False)
                                self.receive_id = rec.picking_id.id
                                self.vehicle_id.lot_id = lot_obj.id
                    # else:
                    #     for rec in receive.move_ids_without_package:
                    #         if rec.product_id == self.purchase_line_id.product_id:
                    #             rec.picking_id.pending_delivery_id = self.id
                    #             self.receive_id = rec.picking_id.id
                    #             if rec.lot_ids:
                    #                 self.vehicle_id.lot_id = rec.lot_ids.id
            self.vehicle_id.license_plate = self.car_plate_no

    def action_next_stage(self):
        if self.state == 'draft':
            return self.write({'state': 'bank_papers'})
        elif self.state == 'bank_papers':
            return self.write({'state': 'registration'})
        elif self.state == 'registration':
            self.vehicle_id.vin_sn = self.chassis_number
            return self.write({'state': 'policy'})
        elif self.state == 'policy':
            return self.write({'state': 'insurance'})
        elif self.state == 'insurance':
            return self.write({'state': 'licence'})
        elif self.state == 'licence':
            return self.write({'state': 'done'})
        # elif self.state == 'insurance':
        #     # self.vehicle_id.license_plate = self.car_plate_no
        #     if self.receive_ids:
        #         for receive in self.receive_ids:
        #             if receive.state != 'done':
        #                 for rec in receive.move_ids_without_package:
        #                     if rec.product_id == self.purchase_line_id.product_id:
        #                         lot_obj = self.env['stock.production.lot'].create(
        #                             {'name': self.car_plate_no or '' + '/' + self.env[
        #                                 'stock.production.lot']._get_next_serial(
        #                                 rec.company_id,
        #                                 rec.product_id) or
        #                                      self.env['ir.sequence'].next_by_code('stock.lot.serial'),
        #                              'product_id': rec.product_id.id,
        #                              'company_id': rec.company_id.id,
        #                              # 'product_qty': rec.product_uom_qty,
        #                              'vehicle_id': self.vehicle_id.id, })
        #                         rec.lot_ids = [(4, lot_obj.id)]
        #                         rec.picking_id.pending_delivery_id = self.id
        #                         rec._action_done(cancel_backorder=False)
        #                         self.receive_id = rec.picking_id.id
        #                 # receive.with_context(cancel_backorder=False)._action_done()
        #     return self.write({'state': 'done'})
        else:
            return True

    def action_back_stage(self):
        if self.state == 'bank_papers':
            return self.write({'state': 'draft'})
        elif self.state == 'insurance':
            return self.write({'state': 'policy'})
        elif self.state == 'policy':
            self.vehicle_id.vin_sn = self.chassis_number
            return self.write({'state': 'registration'})
        elif self.state == 'registration':
            return self.write({'state': 'bank_papers'})
        elif self.state == 'licence':
            self.vehicle_insurance_id.unlink()
            return self.write({'state': 'insurance'})
        elif self.state == 'done':
            self.vehicle_id.license_plate = self.car_plate_no
            return self.write({'state': 'licence'})
        else:
            return True

    @api.depends('purchase_line_id', 'vehicle_price')
    def compute_vehicle_price_incl(self):
        for rec in self:
            all_taxes = 0.0
            if rec.purchase_line_id.taxes_id:
                for tax in rec.purchase_line_id.taxes_id:
                    all_taxes += tax.amount / 100
            if all_taxes:
                rec.vehicle_price_incl = rec.vehicle_price * all_taxes
            else:
                rec.vehicle_price_incl = 0.0

    @api.depends('vehicle_price', 'vehicle_price_incl')
    def compute_car_po_price(self):
        for rec in self:
            rec.car_po_price = rec.vehicle_price + rec.vehicle_price_incl

    @api.depends('purchase_id')
    def get_purchase_picking(self):
        for rec in self:
            if rec.purchase_id:
                rec.receive_ids = [(6, 0, rec.purchase_id.picking_ids.ids)]
            else:
                rec.receive_ids = [()]
