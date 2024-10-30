import datetime

from odoo import api, fields, models, _
from odoo.tools import float_round
from odoo.exceptions import UserError
import pytz

FUEL_SELECTION = [
    ('1/8', '1/8'),
    ('2/8', '2/8'),
    ('3/8', '3/8'),
    ('4/8', '4/8'),
    ('5/8', '5/8'),
    ('6/8', '6/8'),
    ('7/8', '7/8'),
    ('8/8', '8/8'),
]


def time_to_float(t):
    return float_round(t.hour + t.minute / 60 + t.second / 3600, precision_digits=2)


class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    engine_number = fields.Char()


STATE_SELECTION = [
    ('draft', 'draft'),
    ('sent', 'Request Sent'),
    ('inprogress', 'In Progress'),
    ('renew', 'To Renew'),
    ('closed', 'Closed')
]
SELECTION_VALS = [s[0] for s in STATE_SELECTION]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    car_id = fields.Many2one(comodel_name="car.rental.agreement", string="", required=False, )


class CarMove(models.Model):
    _name = 'car.move'
    _description = 'Car Move'

    car_move = fields.Selection(string="", selection=[('in', 'Car In'), ('out', 'Car Out'), ])
    driver_id = fields.Many2one(comodel_name="hr.employee")
    # vehicle_id = fields.Many2one("fleet.vehicle", string="Plate Number", related='serial_id.vehicle_id', readonly=0)
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle", related='serial_id.vehicle_id', readonly=0)
    date = fields.Datetime(string="Date", required=False, )
    km_reading = fields.Float(related='vehicle_id.odometer', readonly=False, string='KM Reading')
    fuel = fields.Selection(string="", selection=FUEL_SELECTION, required=False, )
    source_location_id = fields.Many2one(comodel_name="stock.location", string="Source Location",
                                         domain=[('usage', '=', 'internal')])
    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        required=False,
        copy=True,
        domain=[('usage', '=', 'internal')]
    )
    # operation_type = fields.Many2one('stock.picking.type', domain=[('code', '=', 'internal')], readonly=0,
    #                                  string='Operation Type')
    operation_type = fields.Many2one('stock.picking.type',readonly=0,
                                     string='Operation Type')
    # serial_id = fields.Many2one(comodel_name='stock.production.lot', string="Lot/Serial", readonly=False, )
    serial_id = fields.Many2one(comodel_name='stock.production.lot', string="Plate Number", readonly=False, )
    garage_serial = fields.Char(string="Garage Serial")
    car_rent_id = fields.Many2one(comodel_name="car.rental", string="", required=False, )
    lease_id = fields.Many2one(comodel_name="lease.agree", string="", required=False, )
    replacement_id = fields.Many2one(comodel_name="replacement.model", string="", required=False, )
    non_replacement_id = fields.Many2one(comodel_name="non_replacement.model", string="", required=False, )
    prelease_id = fields.Many2one(comodel_name="pre.lease", string="", required=False, )
    contract_id = fields.Many2one(comodel_name="short.contract", string="", required=False, )
    out_source_id = fields.Many2one(comodel_name="out.source", string="", required=False, )
    is_created = fields.Boolean(string="", )

    def create_stock_move(self):
        source = self.lease_id.name or self.out_source_id.name or self.prelease_id.name or self.car_rent_id.name or self.contract_id.name or self.non_replacement_id.name or self.replacement_id.name
        print(source, 'source====')
        vals = {
            'origin': source,
            'scheduled_date': self.date,
            'location_dest_id': self.dest_location_id.id,
            'location_id': self.source_location_id.id,
            'picking_type_id': self.operation_type.id,
            'move_ids_without_package':
                [(0, 0, {
                    'name': self.serial_id.product_id.name,
                    'product_id': self.serial_id.product_id.id,
                    'product_uom': self.serial_id.product_id.uom_id.id,
                    'location_id': self.source_location_id.id,
                    'location_dest_id': self.dest_location_id.id,
                    'lot_ids': [(4, self.serial_id.id)],
                    'quantity_done': 1,
                    'year_id': self.serial_id.vehicle_id.year_id.id,
                    'odometer_value': self.km_reading,
                    'model_m_id': self.serial_id.vehicle_id.model_id.id,
                    'make_m_id': self.serial_id.vehicle_id.brand_id.id,
                    'category_m_id': self.serial_id.vehicle_id.model_id.category_id.id,
                    'car_identity_ids': [(4, self.serial_id.car_identity_id.id)]
                })],

        }
        picking = self.env['stock.picking'].create(vals)
        self.write({
            'garage_serial': picking.name,
            'is_created': True
        })


class CarRentalAgreement(models.AbstractModel):
    _name = 'car.rental.agreement'
    _inherit = [
        'mail.activity.mixin',

    ]
    _rec_name = 'name'
    _description = 'Car Rental Arguments'

    state = fields.Selection(STATE_SELECTION, required=False, default="draft")

    # def next_stage(self):
    #     index = SELECTION_VALS.index(self.state)
    #     if index != len(SELECTION_VALS) - 1:
    #         self.state = SELECTION_VALS[index + 1]

    def next_stage(self):
        for rec in self:
            index = SELECTION_VALS.index(rec.state)
            if index != len(SELECTION_VALS) - 1:
                rec.state = SELECTION_VALS[index + 1]
                if rec.state == 'closed':
                    # ---------------- closedddddddddddd state -----------------
                    # closed_date = fields.date.today()
                    closed_date = rec.closed_date
                    if rec.vo_id and closed_date:
                        if rec.vo_id.vehicle_payments:
                            vehicle_payments_invoices = rec.vo_id.vehicle_payments.filtered(lambda
                                                                                                p: p.date_from <= closed_date and p.date_to >= closed_date and p.vehicle_licence.id == rec.vehicle_id.id)
                            vehicle_payments_invoices_to_delete = rec.vo_id.vehicle_payments.filtered(lambda
                                                                                                          p: p.date_from > closed_date and p.date_to > closed_date and p.vehicle_licence.id == rec.vehicle_id.id)
                            if vehicle_payments_invoices:
                                vehicle_payments_invoices.date_to = closed_date
                            if vehicle_payments_invoices_to_delete:
                                vehicle_payments_invoices_to_delete.unlink()
                        if rec.vo_id.millage_car_details_ids:
                            vehicle_millage_invoices = rec.vo_id.millage_car_details_ids.filtered(lambda
                                                                                                      p: p.date_from <= closed_date and p.date_to >= closed_date and p.vehicle_licence.id == rec.vehicle_id.id)
                            vehicle_millage_invoices_to_delete = rec.vo_id.millage_car_details_ids.filtered(lambda
                                                                                                                p: p.date_from > closed_date and p.date_to > closed_date and p.vehicle_licence.id == rec.vehicle_id.id)

                            if vehicle_millage_invoices:
                                vehicle_millage_invoices.date_to = closed_date
                            if vehicle_millage_invoices_to_delete:
                                vehicle_millage_invoices_to_delete.unlink()
                    # else:
                    #     raise UserError('You Must Set Closed Date and VO')
                    # ----------------end closedddddddddddd state-----------------

    def prev_stage(self):
        index = SELECTION_VALS.index(self.state)
        if index != 0:
            self.state = SELECTION_VALS[index - 1]

    def action_request_sent(self):
        self.state = 'sent'

    @api.depends('vehicle_id')
    def get_vo_vo_startDate_vo_endDate(self):
        print(f'in get_vo_vo_startDate_vo_endDate')
        for rec in self:
            if rec.vehicle_id:
                if rec.vehicle_id.vo_id:
                    rec.vo_id = rec.vehicle_id.vo_id.id

                # ========MLA ======
                if rec.vehicle_id.mla_id:
                    rec.mla_id = rec.vehicle_id.mla_id.id
                    rec.mla_start_date = rec.vehicle_id.mla_id.start_date
                    rec.mla_end_date = rec.vehicle_id.mla_id.end_date
            #     else:
            #         rec.mla_id = False
            #         rec.mla_start_date = False
            #         rec.mla_end_date = False
            # else:
            #     rec.mla_id = False
            #     rec.mla_start_date = False
            #     rec.mla_end_date = False
            #
    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    customer_id = fields.Many2one(comodel_name="res.partner", required=True)
    contract_id = fields.Many2one("mla.data", 'Contract Number')
    contact_id = fields.Many2one(comodel_name="res.partner", required=False,
                                 domain=[('company_type', '=', 'person')])
    vo_id = fields.Many2one(comodel_name="vehicle.order", string="Vo", required=False,compute='get_vo_vo_startDate_vo_endDate',readonly=False,store=True)
    # vo_start_date = fields.Date(related='vo_id.vo_end_date',compute='get_vo_vo_startDate_vo_endDate')
    # vo_end_date = fields.Date(related='vo_id.vo_start_date',compute='get_vo_vo_startDate_vo_endDate')
    vo_start_date = fields.Date(related='vo_id.vo_start_date',)
    vo_end_date = fields.Date(related='vo_id.vo_end_date',)

    # mla_id = fields.Many2one(related="vo_id.mla_id", string='MLA',compute='get_vo_vo_startDate_vo_endDate')
    mla_id = fields.Many2one("mla.data", string='MLA')
    # mla_id = fields.Many2one(related="vo_id.mla_id", string='MLA')
    # mla_id = fields.Many2one(related="vo_id.rec.vehicle_id.mla_id", string='MLA')
    # mla_id = fields.Many2one('mla.data', string='MLA',compute='get_vo_vo_startDate_vo_endDate',store=True)
    mla_start_date = fields.Date(related='mla_id.start_date')
    mla_end_date = fields.Date(related='mla_id.end_date')
    fleet_in = fields.Many2one(comodel_name="stock.move", string="", required=False, )
    fleet_out = fields.Many2one(comodel_name="stock.move", string="", required=False, )
    user_id = fields.Char()
    license_number = fields.Char()
    license_issue_place = fields.Char()

    # vehicle_order = fields.Many2one(comodel_name="vehicle.order", string="VO")
    # vehicle_id = fields.Many2one("fleet.vehicle", string="Plate Number")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    vin_number = fields.Char(related='vehicle_id.vin_sn')
    vehicle_model = fields.Many2one('fleet.vehicle.model', related='vehicle_id.model_id', string='Make/Model')
    vehicle_color = fields.Char(string='Color', related='vehicle_id.color')
    engine_number = fields.Char(related='vehicle_id.engine_number')
    child_ids = fields.One2many(related='customer_id.child_ids', inverse_name="car_id", string="", required=False, )

    owner_name = fields.Char()
    # customer
    user_name = fields.Many2one('res.partner', domain="[('id','in',child_ids)]")
    email = fields.Char(related='user_name.email')
    id_expiry_date = fields.Date(string='ID Expiry Date')
    closed_date = fields.Date(string='Closed Date',readonly=False,default=fields.date.today())
    license_expiry_date = fields.Date()
    extra_km_rate = fields.Float()

    @api.onchange('vo_id')
    def onchange_extra_km_rate(self):
        self.ensure_one()
        self.extra_km_rate = self.vo_id.extra_km
        self.mla_id = self.vo_id.mla_id.id
        self.mla_start_date = self.vo_id.mla_id.start_date
        self.mla_end_date = self.vo_id.mla_id.end_date

    car_out = fields.Many2one('stock.picking')
    date_out = fields.Date(compute='get_date_time_out')
    time_out = fields.Float(compute='get_date_time_out')  # widget='float_time'
    km_reading_out = fields.Float()
    fuel_out = fields.Selection(FUEL_SELECTION)
    car_in = fields.Many2one('stock.picking')
    date_in = fields.Date(compute='get_date_time_in')
    time_in = fields.Float(compute='get_date_time_in')  # widget='float_time'
    km_reading_in = fields.Float()
    fuel_in = fields.Selection(FUEL_SELECTION)

    #  Vehicle Accessories & Equipment’s
    screwdrivers_out = fields.Boolean()
    jack_hummer_out = fields.Boolean()
    tyre_spanner_out = fields.Boolean()
    first_aid_out = fields.Boolean()
    hazard_triangle_out = fields.Boolean()
    spare_tyre_out = fields.Boolean()
    fire_ext_out = fields.Boolean()
    boot_mats_out = fields.Boolean()
    license_out = fields.Boolean()
    cigarette_tray_out = fields.Boolean()
    cigarette_lighter_out = fields.Boolean()
    cassette_cd_out = fields.Boolean()
    ac_pots_out = fields.Boolean()
    sun_visors_out = fields.Boolean()
    inside_mirror_out = fields.Boolean()
    sun_roof_out = fields.Boolean()
    window_buttons_out = fields.Boolean()
    outside_mirror_button_out = fields.Boolean()
    antenna_out = fields.Boolean()
    wipers_out = fields.Boolean()
    hub_caps_out = fields.Boolean()
    tyre_check_out = fields.Boolean()
    cleanness_out_out = fields.Boolean()
    cleanness_in_out = fields.Boolean()

    screwdrivers_in = fields.Boolean()
    jack_hummer_in = fields.Boolean()
    tyre_spanner_in = fields.Boolean()
    first_aid_in = fields.Boolean()
    hazard_triangle_in = fields.Boolean()
    spare_tyre_in = fields.Boolean()
    fire_ext_in = fields.Boolean()
    boot_mats_in = fields.Boolean()
    license_in = fields.Boolean()
    cigarette_tray_in = fields.Boolean()
    cigarette_lighter_in = fields.Boolean()
    cassette_cd_in = fields.Boolean()
    ac_pots_in = fields.Boolean()
    sun_visors_in = fields.Boolean()
    inside_mirror_in = fields.Boolean()
    sun_roof_in = fields.Boolean()
    window_buttons_in = fields.Boolean()
    outside_mirror_button_in = fields.Boolean()
    antenna_in = fields.Boolean()
    wipers_in = fields.Boolean()
    hub_caps_in = fields.Boolean()
    tyre_check_in = fields.Boolean()
    cleanness_out_in = fields.Boolean()
    cleanness_in_in = fields.Boolean()

    check_out_comments = fields.Text()
    check_in_comments = fields.Text()
    km_included_per_month = fields.Float()
    damage_charge = fields.Float()

    @api.depends('car_out')
    def get_date_time_out(self):
        for rec in self:
            if rec.car_out:
                rec.date_out = rec.car_out.date.date()
                utc_time = pytz.UTC.localize(rec.car_out.date)
                user_tz_time = utc_time.astimezone(pytz.timezone(self._context.get('tz', self.env.user.tz)))
                rec.time_out = time_to_float(user_tz_time)
            else:
                rec.date_out = False
                rec.time_out = False

    @api.depends('car_in')
    def get_date_time_in(self):
        for rec in self:
            if rec.car_in:
                rec.date_in = rec.car_in.date.date()
                utc_time = pytz.UTC.localize(rec.car_in.date)
                user_tz_time = utc_time.astimezone(pytz.timezone(self._context.get('tz', self.env.user.tz)))
                rec.time_in = time_to_float(user_tz_time)
            else:
                rec.date_in = False
                rec.time_in = False

    @api.model
    def get_report_name(self):
        'please override this'
        return ''

    # @api.depends('vehicle_id')
    # def get_vo_vo_startDate_vo_endDate(self):
    #     print(f'in get_vo_vo_startDate_vo_endDate')
    #     for rec in self:
    #         if rec.vehicle_id:
    #             if rec.vehicle_id.vo_id:
    #                 rec.vo_id = rec.vehicle_id.vo_id.id
    #                 if rec.vehicle_id.vo_id.vo_start_date:
    #                     rec.vo_start_date = rec.vehicle_id.vo_id.vo_start_date
    #                 else:
    #                     rec.vo_start_date = False
    #                 if rec.vehicle_id.vo_id.vo_end_date:
    #                     rec.vo_end_date = rec.vehicle_id.vo_id.vo_end_date
    #                 else:
    #                     rec.vo_end_date = False
    #             else:
    #                 rec.vo_id = False
    #                 rec.vo_start_date = False
    #                 rec.vo_end_date = False
    #
    #             # ========MLA ======
    #             if rec.vehicle_id.mla_id:
    #                 rec.mla_id = rec.vehicle_id.mla_id.id
    #                 if rec.vehicle_id.mla_id.start_date:
    #                     rec.mla_start_date = rec.vehicle_id.mla_id.start_date
    #                 else:
    #                     rec.mla_start_date = False
    #                 if rec.vehicle_id.mla_id.end_date:
    #                     rec.mla_end_date = rec.vehicle_id.mla_id.end_date
    #                 else:
    #                     rec.mla_end_date = False
    #             else:
    #                 rec.mla_id = False
    #                 rec.mla_start_date = False
    #                 rec.mla_end_date = False
    #         else:
    #             rec.vo_id = False
    #             rec.mla_id = False
    #             rec.vo_start_date = False
    #             rec.vo_end_date = False
    # # mla_id
    # mla_start_date
    # mla_end_date
