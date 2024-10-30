# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, is_html_empty


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    plate_lot_id = fields.Many2one('stock.production.lot', string="Plate Number")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Lot Vehicle ID", related="plate_lot_id.vehicle_id",
                                 store=True)
    model_id = fields.Many2one('fleet.vehicle.model', 'MMC', related="vehicle_id.model_id",
                               store=True)

    vehicle_id2 = fields.Many2one("fleet.vehicle", string="Vehicle ID")

    # vo_id = fields.Many2one("vehicle.order", string='VO', domain="[('state', 'in', ['inprogress','confirmed'])]", )
    vo_id = fields.Many2one("vehicle.order", string='VO', domain="[('state', 'in', ['inprogress','confirmed'])]",
                            related='plate_lot_id.vehicle_id.vo_id',store=True)
    customer_id = fields.Many2one(comodel_name="res.partner", related="vo_id.customer_id", store=True)

    # mla_id = fields.Many2one(comodel_name="mla.data", string="MLA")
    # mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", related='plate_lot_id.vehicle_id.mla_id',store=True)
    mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", compute='get_plate_lot_id_mla',store=True)
    # no_tire = fields.Float(string="No. Of Tire")
    # model_id = fields.Many2one("fleet.vehicle.model", string="Models")
    service_center_id = fields.Many2one('res.partner', string="Service Center",
                                        domain=[('is_company', '=', True)])
    service_center_mobile = fields.Char(related="service_center_id.mobile", store=True,
                                        string="Service Center Mobile Number")

    service_center_add_id = fields.Many2one('res.partner', string="Service Center Address", domain=lambda self: [
        ('id', 'in', self.service_center_id.child_ids.filtered(lambda x: x.type == 'delivery').ids)], )
    service_center_contact_id = fields.Many2one('res.partner', string="Service Center Contact", domain=lambda self: [
        ('id', 'in', self.service_center_id.child_ids.filtered(lambda x: x.type == 'contact').ids)])
    service_center_contact_mobile = fields.Char(related="service_center_contact_id.mobile", store=True,
                                                string="Service Center Contact Mobile Number")

    billing_method = fields.Selection([
        ('after_repair', 'After Repair'),
        ('before_repair', 'Before Repair'),
        ('no_bill', 'No Bill')], string='Billing Method',
        copy=False, default='no_bill', tracking=True)
    bill_count = fields.Integer(string='Bills', compute='_compute_bill_count')
    bill_ids = fields.One2many('account.move', 'repair_vb_id', string='Bills', copy=False)
    partner_id = fields.Many2one(
        'res.partner', 'Customer', domain="[('id', '=', customer_id)]",
        index=True, states={'confirmed': [('readonly', True)]}, check_company=True, change_default=True,
        help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.')
    show_bill_button = fields.Boolean(copy=False, compute='compute_show_bill_button', store=True)
    km_in = fields.Float('KM In')
    km_out = fields.Float('Km Out')
    km_date_in = fields.Date('Km Date In')
    km_date_out = fields.Date('Km Date Out')
    odometer_created = fields.Boolean(copy=False)
    product_id = fields.Many2one(
        'product.product', string='Car Brand',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        readonly=True, required=True, states={'draft': [('readonly', False)]}, check_company=True)
    mobile_phone = fields.Char(related='user_id.employee_id.mobile_phone', store=True, string="Mobile Number")
    custom_repair_type = fields.Selection([
        ('predictive', 'Predictive'),
        ('corrective', 'Corrective'),
        ('both', 'Both'),('battery', 'Battery'),('tire', 'Tire')], string='Repair Type',
        copy=False, tracking=True)
    maintenance_engineer_id = fields.Many2one('hr.employee', string="Maintenance Engineer")
    emp_work_email = fields.Char(related='maintenance_engineer_id.work_email', store=True)
    emp_mobile_phone = fields.Char(related='maintenance_engineer_id.mobile_phone', store=True)
    maintenance_quality_id = fields.Many2one('hr.employee', string="Maintenance & quality Manager")
    quality_work_email = fields.Char(related='maintenance_quality_id.work_email', store=True)
    quality_mobile_phone = fields.Char(related='maintenance_quality_id.mobile_phone', store=True)
    maintenance_supervisor_id = fields.Many2one('hr.employee', string="Maintenance Supervisor")
    supervisor_work_email = fields.Char(related='maintenance_supervisor_id.work_email', store=True)
    supervisor_mobile_phone = fields.Char(related='maintenance_supervisor_id.mobile_phone', store=True)
    maintenance_plan_id = fields.Many2one('maintenance.schedule.plan', string="Schedule Repair",
                                          domain="[('done', '=', 'no'),('vehicle_id', '=', vehicle_id)]")
    next_maintenance_km = fields.Float('Next Maintenance KM', compute="get_next_maintenance_km", store=True)
    is_vo = fields.Boolean()

    @api.depends('km_out', 'maintenance_plan_id', 'maintenance_plan_id.km_maintenance')
    def get_next_maintenance_km(self):
        for rec in self:
            if rec.maintenance_plan_id:
                next_maintenance_plan_obj = self.env['maintenance.schedule.plan'].search(
                    [('id', '>', rec.maintenance_plan_id.id)], limit=1)
                rec.next_maintenance_km = rec.km_out - rec.maintenance_plan_id.km_maintenance + next_maintenance_plan_obj.km_maintenance
            else:
                rec.next_maintenance_km = rec.km_out

    def create_odometer(self):
        for rec in self:
            odometer_in_obj = False
            odometer_out_obj = False
            if rec.km_in and rec.km_date_in and rec.vehicle_id:
                odometer_in_obj = self.env['fleet.vehicle.odometer'].create({
                    'date': rec.km_date_in,
                    'value': rec.km_in,
                    'vehicle_id': rec.vehicle_id.id or rec.vehicle_id2.id,
                })
            if rec.km_out and rec.km_date_out and rec.vehicle_id:
                odometer_out_obj = self.env['fleet.vehicle.odometer'].create({
                    'date': rec.km_date_out,
                    'value': rec.km_out,
                    'vehicle_id': rec.vehicle_id.id or rec.vehicle_id2.id,
                })
            if odometer_in_obj or odometer_out_obj:
                rec.odometer_created = True

    @api.onchange('service_center_id')
    def _onchange_service_center_id(self):
        return {
            'domain': {
                'service_center_add_id': [
                    ('id', 'in', self.service_center_id.child_ids.filtered(lambda x: x.type == 'delivery').ids)],
                'service_center_contact_id': [
                    ('id', 'in', self.service_center_id.child_ids.filtered(lambda x: x.type == 'contact').ids)],
            }
        }

    @api.onchange('plate_lot_id')
    def _onchange_plate_lot_id(self):
        if self.plate_lot_id:
            self.product_id = self.plate_lot_id.product_id.id
            self.lot_id = self.plate_lot_id.id

        else:
            self.product_id = False
            self.lot_id = False
            self.mla_id = False

    @api.depends('plate_lot_id')
    def get_plate_lot_id_mla(self):
        if self.plate_lot_id:
            if self.plate_lot_id.vehicle_id:
                if self.plate_lot_id.vehicle_id.mla_id:
                    self.mla_id = self.plate_lot_id.vehicle_id.mla_id.id
                else:
                    self.mla_id = False
            else:
                self.mla_id = False
        else:
            self.mla_id = False

    # @api.depends('vo_id')
    # @api.onchange('vo_id')
    # def _onchange_vo_id(self):
    #     if self.vo_id:
    #         self.mla_id = self.vo_id.mla_id.id
    #     else:
    #         self.mla_id = False

    def _compute_bill_count(self):
        for repair_id in self:
            move_ids = repair_id.env['account.move'].search([('repair_vb_id', '=', self.id)])
            if move_ids:
                self.bill_count = len(move_ids)
            else:
                self.bill_count = 0

    def create_bill(self):
        for repair_id in self:
            current_user = self.env.uid
            narration = repair_id.quotation_notes
            currency = repair_id.pricelist_id.currency_id
            company = repair_id.env.company
            purchase_journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
            # journal = repair_id.env['account.move'].with_context(move_type='in_invoice')._get_default_journal()
            # print("sdsds", journal)
            # if not journal:
            #     raise UserError(_('Please define an accounting Purchase journal for the company %s (%s).') % (
            #         company.name, company.id))

            repair_id.env['account.move'].create({'move_type': 'in_invoice',
                                                  'invoice_origin': repair_id.name,
                                                  'invoice_user_id': current_user,
                                                  'narration': narration,
                                                  'partner_id': repair_id.service_center_id.id,
                                                  'currency_id': currency.id,
                                                  'journal_id': purchase_journal.id,
                                                  'payment_reference': repair_id.name,
                                                  # 'invoice_line_ids': [],
                                                  'is_repair_order_bill': True,
                                                  'repair_vb_id': repair_id.id
                                                  })
            Bills = self.bill_ids
            # Create Bill lines from operations.
            for operation in repair_id.operations.filtered(lambda op: op.type == 'add'):
                name = operation.name

                account = operation.product_id.product_tmpl_id._get_product_accounts()['income']
                if not account:
                    raise UserError(_('No account defined for product "%s".', operation.product_id.name))

                invoice_line_vals = {
                    'name': name,
                    'account_id': account.id,
                    'quantity': operation.product_uom_qty,
                    'tax_ids': [(6, 0, operation.tax_id.ids)],
                    'product_uom_id': operation.product_uom.id,
                    'price_unit': operation.price_unit,
                    'product_id': operation.product_id.id,
                    'repair_line_ids': [(4, operation.id)],
                }

                if currency == company.currency_id:
                    balance = -(operation.product_uom_qty * operation.price_unit)
                    invoice_line_vals.update({
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                    })
                else:
                    amount_currency = -(operation.product_uom_qty * operation.price_unit)
                    balance = currency._convert(amount_currency, company.currency_id, company, fields.Date.today())
                    invoice_line_vals.update({
                        'amount_currency': amount_currency,
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                        'currency_id': currency.id,
                    })
                self.bill_ids.invoice_line_ids = [(0, 0, invoice_line_vals)]

            # Create Bills lines from fees.
            for fee in repair_id.fees_lines:
                name = fee.name

                if not fee.product_id:
                    raise UserError(_('No product defined on fees.'))

                account = fee.product_id.product_tmpl_id._get_product_accounts()['income']
                if not account:
                    raise UserError(_('No account defined for product "%s".', fee.product_id.name))

                invoice_line_vals = {
                    'name': name,
                    'account_id': account.id,
                    'quantity': fee.product_uom_qty,
                    'tax_ids': [(6, 0, fee.tax_id.ids)],
                    'product_uom_id': fee.product_uom.id,
                    'price_unit': fee.price_unit,
                    'product_id': fee.product_id.id,
                    'repair_fee_ids': [(4, fee.id)],
                }

                if currency == company.currency_id:
                    balance = -(fee.product_uom_qty * fee.price_unit)
                    invoice_line_vals.update({
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                    })
                else:
                    amount_currency = -(fee.product_uom_qty * fee.price_unit)
                    balance = currency._convert(amount_currency, company.currency_id, company,
                                                fields.Date.today())
                    invoice_line_vals.update({
                        'amount_currency': amount_currency,
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                        'currency_id': currency.id,
                    })
                self.bill_ids.invoice_line_ids = [(0, 0, invoice_line_vals)]

            result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
            # choose the view_mode accordingly
            if len(Bills) > 1:
                result['domain'] = [('id', 'in', Bills.ids)]
            elif len(Bills) == 1:
                res = self.env.ref('account.view_move_form', False)
                form_view = [(res and res.id or False, 'form')]
                if 'views' in result:
                    result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
                else:
                    result['views'] = form_view
                result['res_id'] = Bills.id
            else:
                result = {'type': 'ir.actions.act_window_close'}

            return result

    def action_open_repair_bill(self):
        return {
            'name': 'Bills',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('repair_vb_id', '=', self.id)],
            'context': {'create': False},
            'target': 'current'
        }

    def action_repair_invoice_create(self):
        for repair in self:
            repair._create_invoices()
            # if repair.invoice_method == 'b4repair':
            #     self.mapped('operations').write({'state': 'confirmed'})

            # repair.action_repair_ready()
            # elif repair.invoice_method == 'after_repair':
            #     repair.write({'state': 'done'})
        return True

    def action_custom_repair_done(self):
        self.maintenance_plan_id.done = 'yes'
        self.maintenance_plan_id.repair_id = self.id
        if self.maintenance_plan_id:
            next_maintenance_plan_obj = self.env['maintenance.schedule.plan'].search(
                [('id', '>', self.maintenance_plan_id.id)], limit=1)
            next_maintenance_plan_obj.km_maintenance = self.next_maintenance_km
        return self.write({'state': 'done'})

    @api.depends('state', 'invoice_method', 'billing_method')
    def compute_show_bill_button(self):
        for rec in self:
            if rec.invoice_method == 'none' and rec.billing_method in ['after_repair',
                                                                       'before_repair'] and rec.state == 'done':
                rec.show_bill_button = True
            elif rec.invoice_method == 'after_repair' and rec.billing_method in ['after_repair',
                                                                                 'before_repair'] and rec.state == '2binvoiced':
                rec.show_bill_button = True
            elif rec.invoice_method == 'b4repair' and rec.billing_method in ['after_repair',
                                                                             'before_repair'] and rec.state == 'ready':
                rec.show_bill_button = True
            else:
                rec.show_bill_button = False

    @api.constrains('operations', 'operations.product_uom_qty', 'operations.price_unit', 'plate_lot_id', 'mla_id',
                    'product_id', 'state')
    def _check_repair_spare_parts(self):
        for rec in self:
            total_tire = 0.0
            if not rec.plate_lot_id:
                raise ValidationError("Plate Number is Required")
            repairs_obj = self.env['repair.order'].search(
                [('plate_lot_id', '=', rec.plate_lot_id.id), ('mla_id', '=', rec.mla_id.id), ('id', '!=', rec.id),
                 ('state', '!=', 'cancel')])
            for repair in repairs_obj:
                for op_line in repair.operations:
                    if op_line.product_id.tire == True:
                        total_tire += op_line.product_uom_qty
            for line in rec.operations:
                if line.product_id.tire == True and line.repair_id.mla_id:
                    all_qty = line.product_uom_qty + total_tire
                    if all_qty > line.repair_id.mla_id.allowed_no_of_tire:
                        if not line.repair_id.partner_id:
                            raise ValidationError("Customer is Required")
                        else:
                            msg = _(
                                "Maximum number of tires exceeded for the Vehicle %s on the contract number %s.") % (
                                      line.repair_id.plate_lot_id.name, line.repair_id.mla_id.name)
                            line.repair_id.message_post(body=msg)
                            if not line.price_unit:
                                raise ValidationError(
                                    _("Maximum number of tires exceeded for the Vehicle %s on the contract number %s and Please set unit price in lines for fees.") % (
                                        line.repair_id.plate_lot_id.name, line.repair_id.mla_id.name))
                    if rec.state == 'done' and rec.vehicle_id.model_id.change_tire_every > 0.0:
                        msg = _(
                            "Automatic schedule activity is set for tire change after %s for vehicle %s.") % (
                                  rec.vehicle_id.model_id.change_tire_every, rec.plate_lot_id.name)
                        rec.message_post(body=msg)

    mail_sent = fields.Boolean(copy=False)

    # @api.model
    # def cron_repair_order(self):
    #     repairs_obj = self.env['repair.order'].search([])
    #     for rec in repairs_obj:
    #         if rec.mail_sent != True and rec.state == 'done':
    #             for line in rec.operations:
    #                 if line.product_id.tire == True and line.repair_id.mla_id and rec.vehicle_id.model_id.change_tire_every > 0.0:
    #                     difference = rec.vehicle_id.odometer - rec.km_out
    #                     if difference > rec.vehicle_id.model_id.change_tire_every:
    #                         users = self.env['res.users'].search([])
    #                         for user in users:
    #                             today = fields.Date.today()
    #                             if user.has_group(
    #                                     'car_maintenance_reminder.maintenance_schedule_group_user') or user.has_group(
    #                                 'car_maintenance_reminder.maintenance_schedule_group_manager'):
    #                                 rec.vehicle_id.activity_schedule(
    #                                     'repair_vendor_bill.schedule_activity_of_send_repair_order_id', today,
    #                                     user_id=user.id,
    #                                     summary=self.env.user.name + ' ' + 'This Vehicle' + ' ' + rec.vehicle_id.name + ' ' + 'exceed every km of mla' + ' ' + line.repair_id.mla_id.name + ' ' + 'of repair order' + ' ' + line.repair_id.name)
    #                         rec.mail_sent = True

    @api.model
    def cron_repair_order(self):
        repairs_obj = self.env['repair.order'].search([])
        # print(f'in cron_repair_order')
        # repair_notified_users = self.env['repair.notified.users'].search([], limit=1)
        # if repair_notified_users:
        #     for user in repair_notified_users.notified_users:
        #         print(f'user id :{user.id}')
        for rec in repairs_obj:
            if rec.mail_sent != True and rec.state == 'done':
                for line in rec.operations:
                    if line.product_id.tire == True and line.repair_id.mla_id and rec.vehicle_id.model_id.change_tire_every > 0.0:
                        difference = rec.vehicle_id.odometer - rec.km_out
                        if difference > rec.vehicle_id.model_id.change_tire_every:
                            # users = self.env['res.users'].search([])
                            repair_notified_users = self.env['repair.notified.users'].search([], limit=1)
                            if repair_notified_users:
                                for user in repair_notified_users.notified_users:
                                    today = fields.Date.today()
                                    # if user.has_group(
                                    #         'car_maintenance_reminder.maintenance_schedule_group_user') or user.has_group(
                                    #     'car_maintenance_reminder.maintenance_schedule_group_manager'):
                                    rec.vehicle_id.activity_schedule(
                                        'repair_vendor_bill.schedule_activity_of_send_repair_order_id', today,
                                        user_id=user.id,
                                        summary=self.env.user.name + ' ' + 'This Vehicle' + ' ' + rec.vehicle_id.name + ' ' + 'exceed every km of mla' + ' ' + line.repair_id.mla_id.name + ' ' + 'of repair order' + ' ' + line.repair_id.name)
                                rec.mail_sent = True

    def action_repair_end(self):
        """ Writes repair order state to 'To be invoiced' if invoice method is
        After repair else state is set to 'Ready'.
        @return: True
        """
        self.maintenance_plan_id.done = 'yes'
        self.maintenance_plan_id.repair_id = self.id
        if self.maintenance_plan_id:
            next_maintenance_plan_obj = self.env['maintenance.schedule.plan'].search(
                [('id', '>', self.maintenance_plan_id.id)], limit=1)
            next_maintenance_plan_obj.km_maintenance = self.next_maintenance_km
        if self.filtered(lambda repair: repair.state != 'under_repair'):
            raise UserError(_("Repair must be under repair in order to end reparation."))
        self._check_product_tracking()
        for repair in self:
            repair.write({'repaired': True})
            vals = {'state': 'done'}
            vals['move_id'] = repair.action_repair_done().get(repair.id)
            if not repair.invoice_id and repair.invoice_method == 'after_repair':
                vals['state'] = '2binvoiced'
            # no_tires = sum([fee_line.product_uom_qty if fee_line.product_id.tire else 0 for fee_line in self.fees_lines])
            # print(f'no_tires 22222 :{no_tires}')
            # vals['no_tire'] = no_tires
            repair.write(vals)

        return True

    def action_repair_done(self):
        """ Creates stock move for operation and stock move for final product of repair order.
        @return: Move ids of final products

        """

        if self.filtered(lambda repair: not repair.repaired):
            raise UserError(_("Repair must be repaired in order to make the product moves."))
        self._check_company()
        self.operations._check_company()
        self.fees_lines._check_company()
        res = {}
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        Move = self.env['stock.move']
        for repair in self:
            # Try to create move with the appropriate owner
            owner_id = False
            available_qty_owner = self.env['stock.quant']._get_available_quantity(repair.product_id, repair.location_id,
                                                                                  repair.lot_id,
                                                                                  owner_id=repair.partner_id,
                                                                                  strict=True)
            if float_compare(available_qty_owner, repair.product_qty, precision_digits=precision) >= 0:
                owner_id = repair.partner_id.id

            moves = self.env['stock.move']
            # for operation in repair.operations:
            #     move = Move.create({
            #         'name': repair.name,
            #         'product_id': operation.product_id.id,
            #         'product_uom_qty': operation.product_uom_qty,
            #         'product_uom': operation.product_uom.id,
            #         'partner_id': repair.address_id.id,
            #         'location_id': operation.location_id.id,
            #         'location_dest_id': operation.location_dest_id.id,
            #         'repair_id': repair.id,
            #         'origin': repair.name,
            #         'company_id': repair.company_id.id,
            #     })
            #
            #     # Best effort to reserve the product in a (sub)-location where it is available
            #     product_qty = move.product_uom._compute_quantity(
            #         operation.product_uom_qty, move.product_id.uom_id, rounding_method='HALF-UP')
            #     available_quantity = self.env['stock.quant']._get_available_quantity(
            #         move.product_id,
            #         move.location_id,
            #         lot_id=operation.lot_id,
            #         strict=False,
            #     )
            #     move._update_reserved_quantity(
            #         product_qty,
            #         available_quantity,
            #         move.location_id,
            #         lot_id=operation.lot_id,
            #         strict=False,
            #     )
            #     # Then, set the quantity done. If the required quantity was not reserved, negative
            #     # quant is created in operation.location_id.
            #     move._set_quantity_done(operation.product_uom_qty)
            #
            #     if operation.lot_id:
            #         move.move_line_ids.lot_id = operation.lot_id
            #
            #     moves |= move
            #     operation.write({'move_id': move.id, 'state': 'done'})
            # move = Move.create({
            #     'name': repair.name,
            #     'product_id': repair.product_id.id,
            #     'product_uom': repair.product_uom.id or repair.product_id.uom_id.id,
            #     'product_uom_qty': repair.product_qty,
            #     'partner_id': repair.address_id.id,
            #     'location_id': repair.location_id.id,
            #     'location_dest_id': repair.location_id.id,
            #     'move_line_ids': [(0, 0, {'product_id': repair.product_id.id,
            #                                'lot_id': repair.lot_id.id,
            #                                'product_uom_qty': 0,  # bypass reservation here
            #                                'product_uom_id': repair.product_uom.id or repair.product_id.uom_id.id,
            #                                'qty_done': repair.product_qty,
            #                                'package_id': False,
            #                                'result_package_id': False,
            #                                'owner_id': owner_id,
            #                                'location_id': repair.location_id.id, #TODO: owner stuff
            #                                'company_id': repair.company_id.id,
            #                                'location_dest_id': repair.location_id.id,})],
            #     'repair_id': repair.id,
            #     'origin': repair.name,
            #     'company_id': repair.company_id.id,
            # })
            # consumed_lines = moves.mapped('move_line_ids')
            # produced_lines = move.move_line_ids
            # moves |= move
            # moves._action_done()
            # produced_lines.write({'consume_line_ids': [(6, 0, consumed_lines.ids)]})
            # res[repair.id] = move.id
        return res
