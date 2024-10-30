from odoo import models, fields, api, _

FUEL_TYPE = [
    ('80', '80'),
    ('92', '92'),
    ('95', '95'),
    ('Natural Gase', 'Natural Gase'),
    ('Electricity', 'Electricity'),

]

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


class AllArgs(models.Model):
    _name = 'all.args'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('all.args') or _('New')
        return super(AllArgs, self).create(vals_list)


class CarRental(models.Model):
    _name = 'car.rental'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'Car Rental'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="car_rent_id", string="", required=False, )

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('car.rental') or _('New')
        # self.env['all.args'].create({
        #     'name': vals_list['name'],
        #     'customer_id': vals_list['customer_id'],
        #     'contract_id':  vals_list['contract_id'],
        #     'contract_id':  vals_list['contact_id'],
        #     'contract_id':  vals_list['vo_id'],
        #     'contract_id':  vals_list['fleet_in'],
        #     'contract_id':  vals_list['fleet_out'],
        #     'contract_id':  vals_list['user_id'],
        #     'contract_id':  vals_list['license_number'],
        #     'contract_id':  vals_list['license_number'],
        #     'contract_id':  vals_list['license_number'],
        #     'contract_id':  vals_list['license_number'],
        #     'contract_id':  vals_list['license_number'],
        #     'contract_id':  vals_list['vehicle_model'],
        #     'contract_id':  vals_list['vin_number'],
        #     'contract_id':  vals_list['vehicle_id'],
        #     'contract_id':  vals_list['license_issue_place'],
        #
        #     'license_issue_place': self.license_issue_place,
        #     'vehicle_id': self.vehicle_id.id,
        #     'vin_number': self.vin_number,
        #     'vehicle_model': self.vehicle_model.id,
        #     'vehicle_color': self.vehicle_color,
        #     'engine_number': self.engine_number,
        #     'child_ids': self.child_ids.ids,
        #     'owner_name': self.owner_name,
        #     'user_name': self.user_name.id,
        #     'email': self.email,
        #     'id_expiry_date': self.id_expiry_date,
        #     'license_expiry_date': self.license_expiry_date,
        #     'extra_km_rate': self.extra_km_rate,
        #     'car_out': self.car_out.id,
        #     'car_in': self.car_in.id,
        #     'date_out': self.date_out,
        #     'time_out': self.time_out,
        #     'km_reading_out': self.km_reading_out,
        #     'fuel_out': self.fuel_out,
        #     'date_in': self.date_in,
        #     'time_in': self.time_in,
        #     'km_reading_in': self.km_reading_in,
        #     'fuel_in': self.fuel_in,
        #     'screwdrivers_out': self.screwdrivers_out,
        #     'jack_hummer_out': self.jack_hummer_out,
        #     'tyre_spanner_out': self.tyre_spanner_out,
        #     'first_aid_out': self.first_aid_out,
        #     'hazard_triangle_out': self.hazard_triangle_out,
        #     'spare_tyre_out': self.spare_tyre_out,
        #     'fire_ext_out': self.fire_ext_out,
        #     'boot_mats_out': self.boot_mats_out,
        #     'license_out': self.license_out,
        #     'cigarette_tray_out': self.cigarette_tray_out,
        #     'cigarette_lighter_out': self.cigarette_lighter_out,
        #     'cassette_cd_out': self.cassette_cd_out,
        #     'ac_pots_out': self.ac_pots_out,
        #     'sun_visors_out': self.sun_visors_out,
        #     'inside_mirror_out': self.inside_mirror_out,
        #     'sun_roof_out': self.sun_roof_out,
        #     'window_buttons_out': self.window_buttons_out,
        #     'outside_mirror_button_out': self.outside_mirror_button_out,
        #     'antenna_out': self.antenna_out,
        #     'wipers_out': self.wipers_out,
        #     'hub_caps_out': self.hub_caps_out,
        #     'tyre_check_out': self.tyre_check_out,
        #     'cleanness_out_out': self.cleanness_out_out,
        #     'cleanness_in_out': self.cleanness_in_out,
        #     'screwdrivers_in': self.screwdrivers_in,
        #     'jack_hummer_in': self.jack_hummer_in,
        #     'tyre_spanner_in': self.tyre_spanner_in,
        #     'first_aid_in': self.first_aid_in,
        #     'hazard_triangle_in': self.hazard_triangle_in,
        #     'spare_tyre_in': self.spare_tyre_in,
        #     'fire_ext_in': self.fire_ext_in,
        #     'boot_mats_in': self.boot_mats_in,
        #     'license_in': self.license_in,
        #     'cigarette_tray_in': self.cigarette_tray_in,
        #     'cassette_cd_in': self.cassette_cd_in,
        #     'ac_pots_in': self.ac_pots_in,
        #     'sun_visors_in': self.sun_visors_in,
        #     'inside_mirror_in': self.inside_mirror_in,
        #     'sun_roof_in': self.sun_roof_in,
        #     'window_buttons_in': self.window_buttons_in,
        #     'outside_mirror_button_in': self.outside_mirror_button_in,
        #     'antenna_in': self.antenna_in,
        #     'wipers_in': self.wipers_in,
        #     'tyre_check_in': self.tyre_check_in,
        #     'cleanness_out_in': self.cleanness_out_in,
        #     'cleanness_in_in': self.cleanness_in_in,
        #     'check_out_comments': self.check_out_comments,
        #     'check_in_comments': self.check_in_comments,
        #     'damage_charge': self.damage_charge,
        #     'km_included_per_month': self.km_included_per_month,
        #
        # })

        return super(CarRental, self).create(vals_list)

    @api.model
    def get_report_name(self):
        return _("Car rental agreement")


class LeaseAgree(models.Model):
    _name = 'lease.agree'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    contact_id = fields.Many2one(comodel_name="res.partner", required=False,
                                 domain=[('company_type', '=', 'person')])
    user_id = fields.Many2one(comodel_name="res.partner", required=False, )
    users_peron = fields.Many2many(comodel_name="res.partner", compute='get_user_person')
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False,
                                  domain=[('company_type', '=', 'company')])
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner ", required=False,
                                 domain=[('company_type', '=', 'person')])

    phone = fields.Char(related='user_id.phone')
    email = fields.Char(related='user_id.email')
    contract_start_date = fields.Date(string="", required=False, )
    contract_end_date = fields.Date(string="", required=False, )
    # vehicle_id = fields.Many2one("fleet.vehicle", string="Plate NO")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    vo_id = fields.Many2one(comodel_name="vehicle.order", string='VO')
    vehicle_model = fields.Many2one('fleet.vehicle.model', related='vehicle_id.model_id', string='Make/Model')
    year_model = fields.Char(related='vehicle_id.model_year', string='Year/Model')
    vehicle_color = fields.Char(string='Color', related='vehicle_id.color')
    engine_number = fields.Char(related='vehicle_id.engine_number')
    vin_number = fields.Char(related='vehicle_id.vin_sn', string='Chassis Number')
    fuel_delivery = fields.Selection(string="", selection=FUEL_SELECTION, required=False, )
    fuel_europcar = fields.Selection(string="", selection=FUEL_SELECTION, required=False, )
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="lease_id", string="", required=False, )

    km_reading_delivery = fields.Float(string=" Km reading on Delivery", required=False, )
    km_reading_europcar = fields.Float(string="Km reading Europcar", required=False, )
    screwdrivers = fields.Boolean(string="", )
    cover = fields.Boolean(string="", )
    head_rest = fields.Boolean(string="", )
    toeing_hook = fields.Boolean(string="", )
    cigarette_ashtray = fields.Boolean(string="", )
    carpets = fields.Boolean(string="", )
    tyre_spanner = fields.Boolean(string="", )
    cigarette_lighter = fields.Boolean(string="", )
    interior_rear = fields.Boolean(string="", )
    Lift = fields.Boolean(string="", )
    license = fields.Boolean(string="", )
    dvd = fields.Boolean(string="", )
    hazard_triangle = fields.Boolean(string="", )
    seat_fabric = fields.Boolean(string="", )
    bluetooth_device = fields.Boolean(string="", )
    aid_kit = fields.Boolean(string="1th Aid Kit", )
    manual_booklet = fields.Boolean(string="", )
    hub_caps = fields.Boolean(string="", )
    fire_ext = fields.Boolean(string="", )
    warranty_booklet = fields.Boolean(string="", )
    antenna = fields.Boolean(string="", )
    lift = fields.Boolean(string="Lift", )
    spare_wheel = fields.Boolean(string="", )
    cassette_cd = fields.Boolean(string="", )
    track_system = fields.Boolean(string="", )
    tyres_type = fields.Boolean(string="4 Tyres type", )
    fuel_type = fields.Selection(selection=FUEL_TYPE)
    stone = fields.Char(string="BRIDGESTONE", required=False, )
    extra_km = fields.Float(string="Extra Kilometers Charges", required=False, )
    excess = fields.Float(string="Damage Charge", required=False, )
    comment = fields.Text(string="Check In Comments", required=False, )

    def get_user_person(self):
        print('==================')
        for rec in self:
            partners = self.env['res.partner'].search([('company_type', '=', 'person')])
            print(partners.mapped('company_type'))

            partner_lst = []
            for partner in partners:
                if partner.company_type == 'person':
                    print(partner.company_type)
                    partner_lst.append(partner.id)

            rec.users_peron = [(6, 0, partner_lst)]

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('lease.agree') or _('New')
        # self.env['all.args'].create({
        #     'name': self.name,
        #     'customer_id': self.customer_id.id,
        #     'contract_id': self.contract_id.id,
        #     'contact_id': self.contact_id.id,
        #     'vo_id': self.vo_id.id,
        #     'fleet_in': self.fleet_in.id,
        #     'fleet_out': self.fleet_out.id,
        #     'user_id': self.user_id,
        #     'license_number': self.license_number,
        #     'license_issue_place': self.license_issue_place,
        #     'vehicle_id': self.vehicle_id.id,
        #     'vin_number': self.vin_number,
        #     'vehicle_model': self.vehicle_model.id,
        #     'vehicle_color': self.vehicle_color,
        #     'engine_number': self.engine_number,
        #     'child_ids': self.child_ids.ids,
        #     'owner_name': self.owner_name,
        #     'user_name': self.user_name.id,
        #     'email': self.email,
        #     'id_expiry_date': self.id_expiry_date,
        #     'license_expiry_date': self.license_expiry_date,
        #     'extra_km_rate': self.extra_km_rate,
        #     'car_out': self.car_out.id,
        #     'car_in': self.car_in.id,
        #     'date_out': self.date_out,
        #     'time_out': self.time_out,
        #     'km_reading_out': self.km_reading_out,
        #     'fuel_out': self.fuel_out,
        #     'date_in': self.date_in,
        #     'time_in': self.time_in,
        #     'km_reading_in': self.km_reading_in,
        #     'fuel_in': self.fuel_in,
        #     'screwdrivers_out': self.screwdrivers_out,
        #     'jack_hummer_out': self.jack_hummer_out,
        #     'tyre_spanner_out': self.tyre_spanner_out,
        #     'first_aid_out': self.first_aid_out,
        #     'hazard_triangle_out': self.hazard_triangle_out,
        #     'spare_tyre_out': self.spare_tyre_out,
        #     'fire_ext_out': self.fire_ext_out,
        #     'boot_mats_out': self.boot_mats_out,
        #     'license_out': self.license_out,
        #     'cigarette_tray_out': self.cigarette_tray_out,
        #     'cigarette_lighter_out': self.cigarette_lighter_out,
        #     'cassette_cd_out': self.cassette_cd_out,
        #     'ac_pots_out': self.ac_pots_out,
        #     'sun_visors_out': self.sun_visors_out,
        #     'inside_mirror_out': self.inside_mirror_out,
        #     'sun_roof_out': self.sun_roof_out,
        #     'window_buttons_out': self.window_buttons_out,
        #     'outside_mirror_button_out': self.outside_mirror_button_out,
        #     'antenna_out': self.antenna_out,
        #     'wipers_out': self.wipers_out,
        #     'hub_caps_out': self.hub_caps_out,
        #     'tyre_check_out': self.tyre_check_out,
        #     'cleanness_out_out': self.cleanness_out_out,
        #     'cleanness_in_out': self.cleanness_in_out,
        #     'screwdrivers_in': self.screwdrivers_in,
        #     'jack_hummer_in': self.jack_hummer_in,
        #     'tyre_spanner_in': self.tyre_spanner_in,
        #     'first_aid_in': self.first_aid_in,
        #     'hazard_triangle_in': self.hazard_triangle_in,
        #     'spare_tyre_in': self.spare_tyre_in,
        #     'fire_ext_in': self.fire_ext_in,
        #     'boot_mats_in': self.boot_mats_in,
        #     'license_in': self.license_in,
        #     'cigarette_tray_in': self.cigarette_tray_in,
        #     'cassette_cd_in': self.cassette_cd_in,
        #     'ac_pots_in': self.ac_pots_in,
        #     'sun_visors_in': self.sun_visors_in,
        #     'inside_mirror_in': self.inside_mirror_in,
        #     'sun_roof_in': self.sun_roof_in,
        #     'window_buttons_in': self.window_buttons_in,
        #     'outside_mirror_button_in': self.outside_mirror_button_in,
        #     'antenna_in': self.antenna_in,
        #     'wipers_in': self.wipers_in,
        #     'tyre_check_in': self.tyre_check_in,
        #     'cleanness_out_in': self.cleanness_out_in,
        #     'cleanness_in_in': self.cleanness_in_in,
        #     'check_out_comments': self.check_out_comments,
        #     'check_in_comments': self.check_in_comments,
        #     'damage_charge': self.damage_charge,
        #     'km_included_per_month': self.km_included_per_month,
        #
        # })

        return super(LeaseAgree, self).create(vals_list)


class GarageDelivery(models.Model):
    _name = 'garage.delivery'
    _inherit = 'car.rental.agreement'

    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('garage.delivery') or _('New')
        # self.env['all.args'].create({
        #     'name': self.name,
        #     'customer_id': self.customer_id.id,
        #     'contract_id': self.contract_id.id,
        #     'contact_id': self.contact_id.id,
        #     'vo_id': self.vo_id.id,
        #     'fleet_in': self.fleet_in.id,
        #     'fleet_out': self.fleet_out.id,
        #     'user_id': self.user_id,
        #     'license_number': self.license_number,
        #     'license_issue_place': self.license_issue_place,
        #     'vehicle_id': self.vehicle_id.id,
        #     'vin_number': self.vin_number,
        #     'vehicle_model': self.vehicle_model.id,
        #     'vehicle_color': self.vehicle_color,
        #     'engine_number': self.engine_number,
        #     'child_ids': self.child_ids.ids,
        #     'owner_name': self.owner_name,
        #     'user_name': self.user_name.id,
        #     'email': self.email,
        #     'id_expiry_date': self.id_expiry_date,
        #     'license_expiry_date': self.license_expiry_date,
        #     'extra_km_rate': self.extra_km_rate,
        #     'car_out': self.car_out.id,
        #     'car_in': self.car_in.id,
        #     'date_out': self.date_out,
        #     'time_out': self.time_out,
        #     'km_reading_out': self.km_reading_out,
        #     'fuel_out': self.fuel_out,
        #     'date_in': self.date_in,
        #     'time_in': self.time_in,
        #     'km_reading_in': self.km_reading_in,
        #     'fuel_in': self.fuel_in,
        #     'screwdrivers_out': self.screwdrivers_out,
        #     'jack_hummer_out': self.jack_hummer_out,
        #     'tyre_spanner_out': self.tyre_spanner_out,
        #     'first_aid_out': self.first_aid_out,
        #     'hazard_triangle_out': self.hazard_triangle_out,
        #     'spare_tyre_out': self.spare_tyre_out,
        #     'fire_ext_out': self.fire_ext_out,
        #     'boot_mats_out': self.boot_mats_out,
        #     'license_out': self.license_out,
        #     'cigarette_tray_out': self.cigarette_tray_out,
        #     'cigarette_lighter_out': self.cigarette_lighter_out,
        #     'cassette_cd_out': self.cassette_cd_out,
        #     'ac_pots_out': self.ac_pots_out,
        #     'sun_visors_out': self.sun_visors_out,
        #     'inside_mirror_out': self.inside_mirror_out,
        #     'sun_roof_out': self.sun_roof_out,
        #     'window_buttons_out': self.window_buttons_out,
        #     'outside_mirror_button_out': self.outside_mirror_button_out,
        #     'antenna_out': self.antenna_out,
        #     'wipers_out': self.wipers_out,
        #     'hub_caps_out': self.hub_caps_out,
        #     'tyre_check_out': self.tyre_check_out,
        #     'cleanness_out_out': self.cleanness_out_out,
        #     'cleanness_in_out': self.cleanness_in_out,
        #     'screwdrivers_in': self.screwdrivers_in,
        #     'jack_hummer_in': self.jack_hummer_in,
        #     'tyre_spanner_in': self.tyre_spanner_in,
        #     'first_aid_in': self.first_aid_in,
        #     'hazard_triangle_in': self.hazard_triangle_in,
        #     'spare_tyre_in': self.spare_tyre_in,
        #     'fire_ext_in': self.fire_ext_in,
        #     'boot_mats_in': self.boot_mats_in,
        #     'license_in': self.license_in,
        #     'cigarette_tray_in': self.cigarette_tray_in,
        #     'cassette_cd_in': self.cassette_cd_in,
        #     'ac_pots_in': self.ac_pots_in,
        #     'sun_visors_in': self.sun_visors_in,
        #     'inside_mirror_in': self.inside_mirror_in,
        #     'sun_roof_in': self.sun_roof_in,
        #     'window_buttons_in': self.window_buttons_in,
        #     'outside_mirror_button_in': self.outside_mirror_button_in,
        #     'antenna_in': self.antenna_in,
        #     'wipers_in': self.wipers_in,
        #     'tyre_check_in': self.tyre_check_in,
        #     'cleanness_out_in': self.cleanness_out_in,
        #     'cleanness_in_in': self.cleanness_in_in,
        #     'check_out_comments': self.check_out_comments,
        #     'check_in_comments': self.check_in_comments,
        #     'damage_charge': self.damage_charge,
        #     'km_included_per_month': self.km_included_per_month,
        #
        # })
        return super(GarageDelivery, self).create(vals_list)


class Replacement(models.Model):
    _name = 'replacement.model'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    customer_id = fields.Many2one(comodel_name="res.partner", required=True, domain="[('customer_rank','>', 0)]")
    phone_number = fields.Char(string="Phone Number", readonly=False, related='contact_id.phone')
    contract_id = fields.Many2one("mla.data", 'Contract Number')
    user_id = fields.Many2one('res.users')
    # vehicle_id_1 = fields.Many2one("fleet.vehicle", string="Plate Number")
    # vehicle_id = fields.Many2one("fleet.vehicle", string="Plate Number")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    # vin_number_1 = fields.Char(related='vehicle_id_1.vin_sn', string='VIN No',compute='get_vo_mla_vehicle1')
    # vin_number_1 = fields.Char(related='vehicle_id_1.vin_sn', string='VIN No',)
    vin_number_1 = fields.Char(related='vehicle_id.vin_sn', string='VIN No',)
    # vehicle_model_1 = fields.Many2one('fleet.vehicle.model', related='vehicle_id_1.model_id', string='Model')
    vehicle_model_1 = fields.Many2one('fleet.vehicle.model', related='vehicle_id.model_id', string='Model')
    # make_1 = fields.Many2one(related='vehicle_id_1.model_id.brand_id', string='Make')
    make_1 = fields.Many2one(related='vehicle_id.model_id.brand_id', string='Make')
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="replacement_id", string="", required=False, )

    # @api.depends('vehicle_id_1')
    # def get_vo_mla_vehicle1(self):
    #     for rec in self:
    #         if rec.vehicle_id_1:
    #             if rec.vehicle_id_1.vo_id:
    #                 rec.vo_id = rec.vehicle_id_1.vo_id.id
    #                 rec.vo_start_date = rec.vehicle_id_1.vo_id.vo_start_date
    #                 rec.vo_end_date = rec.vehicle_id_1.vo_id.vo_end_date
    #             else:
    #                 rec.vo_id = False
    #                 rec.vo_start_date = False
    #                 rec.vo_end_date = False
    #             if rec.vehicle_id_1.mla_id:
    #                 rec.mla_id = rec.vehicle_id_1.mla_id.id
    #                 rec.mla_start_date = rec.vehicle_id_1.mla_id.start_date
    #                 rec.mla_end_date = rec.vehicle_id_1.mla_id.end_date
    #             else:
    #                 rec.mla_id = False
    #                 rec.mla_start_date = False
    #                 rec.mla_end_date = False
    #         else:
    #             rec.vo_id = False
    #             rec.vo_start_date = False
    #             rec.vo_end_date = False
    #             rec.mla_id = False
    #             rec.mla_start_date = False
    #             rec.mla_end_date = False

    # vo_id = fields.Many2one(comodel_name="vehicle.order",related='vehicle_id_1.vo_id', string="Vo", required=False,compute='get_vo_mla_vehicle1' )
    # vo_start_date = fields.Date(compute='get_vo_mla_vehicle1',related='vehicle_id_1.vo_id.vo_start_date')
    # vo_end_date = fields.Date(compute='get_vo_mla_vehicle1',related='vehicle_id_1.vo_id.vo_end_date')
    #
    # mla_id = fields.Many2one(comodel_name="mla.data",related='vehicle_id_1.mla_id', string='MLA',compute='get_vo_mla_vehicle1')
    # mla_start_date = fields.Date(compute='get_vo_mla_vehicle1',related='vehicle_id_1.mla_id.start_date')
    # mla_end_date = fields.Date(compute='get_vo_mla_vehicle1',related='vehicle_id_1.mla_id.end_date')

    # vo_id = fields.Many2one(comodel_name="vehicle.order", string="Vo", required=False,compute='get_vo_mla_vehicle1' )
    # vo_start_date = fields.Date(compute='get_vo_mla_vehicle1',)
    # vo_end_date = fields.Date(compute='get_vo_mla_vehicle1',)
    #
    # mla_id = fields.Many2one(comodel_name="mla.data", string='MLA',compute='get_vo_mla_vehicle1')
    # mla_start_date = fields.Date(compute='get_vo_mla_vehicle1',)
    # mla_end_date = fields.Date(compute='get_vo_mla_vehicle1',)


    # vehicle_id_2 = fields.Many2one("fleet.vehicle", string="Plate Number")
    vehicle_id_2 = fields.Many2one("fleet.vehicle", string="Vehicle")
    vin_number_2 = fields.Char(related='vehicle_id_2.vin_sn', string='VIN No')
    vehicle_model_2 = fields.Many2one('fleet.vehicle.model', related='vehicle_id_2.model_id', string='Model')
    make_2 = fields.Many2one(related='vehicle_id_2.model_id.brand_id', string='Make')
    kilometer_out_1 = fields.Float(string="Kilometer Out", required=False, )
    kilometer_in_1 = fields.Float(string="Kilometer In", required=False, )
    fuel_out_1 = fields.Selection(string="Fuel Out", selection=FUEL_SELECTION, required=False, )
    fuel_in_1 = fields.Selection(string="Fuel/In", selection=FUEL_SELECTION, required=False, )
    fuel_in_2 = fields.Selection(string="Fuel/In", selection=FUEL_SELECTION, required=False, )
    kilometer_out_2 = fields.Float(string="Kilometer Out", required=False, )
    kilometer_in_2 = fields.Float(string="Kilometer In", required=False, )
    fuel_out_2 = fields.Selection(string="Fuel Out", selection=FUEL_SELECTION, required=False, )
    car_out_1 = fields.Many2one('stock.picking', string='Car Out')
    car_in_1 = fields.Many2one('stock.picking', string="Car In")
    date_out_1 = fields.Date(string="Receive date", compute='get_date_out_1')
    date_in_1 = fields.Date(string="Delivery Date", compute='get_date_date_in_1')
    car_out_2 = fields.Many2one('stock.picking', string='Car Out')
    car_in_2 = fields.Many2one('stock.picking', string='Car In')
    date_out_2 = fields.Date(string="Receive date", compute='get_date_out_2')
    date_in_2 = fields.Date(string="Delivery Date", compute='get_date_date_in_2')
    tools_1 = fields.Boolean(string="Tools")
    tools_2 = fields.Boolean(string="Tools")
    jack_hummer_1 = fields.Boolean(string="Jack Hummer")
    triangle_1 = fields.Boolean(string="Triangle")
    aid_kit_1 = fields.Boolean(string="1th Aid Kit")
    fire_ext_1 = fields.Boolean(string="Fire Ext")
    ashtray_1 = fields.Boolean(string="Ashtray")
    cig_1 = fields.Boolean(string="Cig. Lighter")
    antenna_1 = fields.Boolean(string="Antenna")
    spare_1 = fields.Boolean(string="Spare wheel")
    licence_1 = fields.Boolean(string="License")
    cassette_1 = fields.Boolean(string="Cassette")
    seat_1 = fields.Boolean(string="Seat Fabric")

    jack_hummer_2 = fields.Boolean(string="Jack Hummer")
    triangle_2 = fields.Boolean(string="Triangle")
    aid_kit_2 = fields.Boolean(string="1th Aid Kit")
    fire_ext_2 = fields.Boolean(string="Fire Ext")
    ashtray_2 = fields.Boolean(string="Ashtray")
    cig_2 = fields.Boolean(string="Cig. Lighter")
    antenna_2 = fields.Boolean(string="Antenna")
    spare_2 = fields.Boolean(string="Spare wheel")
    licence_2 = fields.Boolean(string="License")
    cassette_2 = fields.Boolean(string="Cassette")
    seat_2 = fields.Boolean(string="Seat Fabric")
    # engine_number_1 = fields.Char(related='vehicle_id_1.engine_number')
    engine_number_1 = fields.Char(related='vehicle_id.engine_number')
    engine_number_2 = fields.Char(related='vehicle_id_2.engine_number')


    @api.depends('car_out_1')
    def get_date_out_1(self):
        for rec in self:
            if rec.car_out_1:
                rec.date_out_1 = rec.car_out_1.date.date()

            else:
                rec.date_out_1 = False

    @api.depends('car_in_1')
    def get_date_date_in_1(self):
        for rec in self:
            if rec.car_in_1:
                rec.date_in_1 = rec.car_in_1.date.date()

            else:
                rec.date_in_1 = False

    @api.depends('car_out_2')
    def get_date_out_2(self):
        for rec in self:
            if rec.car_out_2:
                rec.date_out_2 = rec.car_out_2.date.date()

            else:
                rec.date_out_2 = False

    @api.depends('car_in_2')
    def get_date_date_in_2(self):
        for rec in self:
            if rec.car_in_2:
                rec.date_in_2 = rec.car_in_2.date.date()

            else:
                rec.date_in_2 = False

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('replacement.model') or _('New')
        # self.env['all.args'].create({
        #     'name': self.name,
        #     'customer_id': self.customer_id.id,
        #     'contract_id': self.contract_id.id,
        #     'contact_id': self.contact_id.id,
        #     'vo_id': self.vo_id.id,
        #     'fleet_in': self.fleet_in.id,
        #     'fleet_out': self.fleet_out.id,
        #     'user_id': self.user_id,
        #     'license_number': self.license_number,
        #     'license_issue_place': self.license_issue_place,
        #     'vehicle_id': self.vehicle_id.id,
        #     'vin_number': self.vin_number,
        #     'vehicle_model': self.vehicle_model.id,
        #     'vehicle_color': self.vehicle_color,
        #     'engine_number': self.engine_number,
        #     'child_ids': self.child_ids.ids,
        #     'owner_name': self.owner_name,
        #     'user_name': self.user_name.id,
        #     'email': self.email,
        #     'id_expiry_date': self.id_expiry_date,
        #     'license_expiry_date': self.license_expiry_date,
        #     'extra_km_rate': self.extra_km_rate,
        #     'car_out': self.car_out.id,
        #     'car_in': self.car_in.id,
        #     'date_out': self.date_out,
        #     'time_out': self.time_out,
        #     'km_reading_out': self.km_reading_out,
        #     'fuel_out': self.fuel_out,
        #     'date_in': self.date_in,
        #     'time_in': self.time_in,
        #     'km_reading_in': self.km_reading_in,
        #     'fuel_in': self.fuel_in,
        #     'screwdrivers_out': self.screwdrivers_out,
        #     'jack_hummer_out': self.jack_hummer_out,
        #     'tyre_spanner_out': self.tyre_spanner_out,
        #     'first_aid_out': self.first_aid_out,
        #     'hazard_triangle_out': self.hazard_triangle_out,
        #     'spare_tyre_out': self.spare_tyre_out,
        #     'fire_ext_out': self.fire_ext_out,
        #     'boot_mats_out': self.boot_mats_out,
        #     'license_out': self.license_out,
        #     'cigarette_tray_out': self.cigarette_tray_out,
        #     'cigarette_lighter_out': self.cigarette_lighter_out,
        #     'cassette_cd_out': self.cassette_cd_out,
        #     'ac_pots_out': self.ac_pots_out,
        #     'sun_visors_out': self.sun_visors_out,
        #     'inside_mirror_out': self.inside_mirror_out,
        #     'sun_roof_out': self.sun_roof_out,
        #     'window_buttons_out': self.window_buttons_out,
        #     'outside_mirror_button_out': self.outside_mirror_button_out,
        #     'antenna_out': self.antenna_out,
        #     'wipers_out': self.wipers_out,
        #     'hub_caps_out': self.hub_caps_out,
        #     'tyre_check_out': self.tyre_check_out,
        #     'cleanness_out_out': self.cleanness_out_out,
        #     'cleanness_in_out': self.cleanness_in_out,
        #     'screwdrivers_in': self.screwdrivers_in,
        #     'jack_hummer_in': self.jack_hummer_in,
        #     'tyre_spanner_in': self.tyre_spanner_in,
        #     'first_aid_in': self.first_aid_in,
        #     'hazard_triangle_in': self.hazard_triangle_in,
        #     'spare_tyre_in': self.spare_tyre_in,
        #     'fire_ext_in': self.fire_ext_in,
        #     'boot_mats_in': self.boot_mats_in,
        #     'license_in': self.license_in,
        #     'cigarette_tray_in': self.cigarette_tray_in,
        #     'cassette_cd_in': self.cassette_cd_in,
        #     'ac_pots_in': self.ac_pots_in,
        #     'sun_visors_in': self.sun_visors_in,
        #     'inside_mirror_in': self.inside_mirror_in,
        #     'sun_roof_in': self.sun_roof_in,
        #     'window_buttons_in': self.window_buttons_in,
        #     'outside_mirror_button_in': self.outside_mirror_button_in,
        #     'antenna_in': self.antenna_in,
        #     'wipers_in': self.wipers_in,
        #     'tyre_check_in': self.tyre_check_in,
        #     'cleanness_out_in': self.cleanness_out_in,
        #     'cleanness_in_in': self.cleanness_in_in,
        #     'check_out_comments': self.check_out_comments,
        #     'check_in_comments': self.check_in_comments,
        #     'damage_charge': self.damage_charge,
        #     'km_included_per_month': self.km_included_per_month,
        #
        # })

        return super(Replacement, self).create(vals_list)

    @api.model
    def get_report_name(self):
        return _("Replacement Vehicle Form")


class PreLease(models.Model):
    _name = 'pre.lease'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="prelease_id", string="", required=False, )

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('pre.lease') or _('New')
        # self.env['all.args'].create({
        #     'name': self.name,
        #     'customer_id': self.customer_id.id,
        #     'contract_id': self.contract_id.id,
        #     'contact_id': self.contact_id.id,
        #     'vo_id': self.vo_id.id,
        #     'fleet_in': self.fleet_in.id,
        #     'fleet_out': self.fleet_out.id,
        #     'user_id': self.user_id,
        #     'license_number': self.license_number,
        #     'license_issue_place': self.license_issue_place,
        #     'vehicle_id': self.vehicle_id.id,
        #     'vin_number': self.vin_number,
        #     'vehicle_model': self.vehicle_model.id,
        #     'vehicle_color': self.vehicle_color,
        #     'engine_number': self.engine_number,
        #     'child_ids': self.child_ids.ids,
        #     'owner_name': self.owner_name,
        #     'user_name': self.user_name.id,
        #     'email': self.email,
        #     'id_expiry_date': self.id_expiry_date,
        #     'license_expiry_date': self.license_expiry_date,
        #     'extra_km_rate': self.extra_km_rate,
        #     'car_out': self.car_out.id,
        #     'car_in': self.car_in.id,
        #     'date_out': self.date_out,
        #     'time_out': self.time_out,
        #     'km_reading_out': self.km_reading_out,
        #     'fuel_out': self.fuel_out,
        #     'date_in': self.date_in,
        #     'time_in': self.time_in,
        #     'km_reading_in': self.km_reading_in,
        #     'fuel_in': self.fuel_in,
        #     'screwdrivers_out': self.screwdrivers_out,
        #     'jack_hummer_out': self.jack_hummer_out,
        #     'tyre_spanner_out': self.tyre_spanner_out,
        #     'first_aid_out': self.first_aid_out,
        #     'hazard_triangle_out': self.hazard_triangle_out,
        #     'spare_tyre_out': self.spare_tyre_out,
        #     'fire_ext_out': self.fire_ext_out,
        #     'boot_mats_out': self.boot_mats_out,
        #     'license_out': self.license_out,
        #     'cigarette_tray_out': self.cigarette_tray_out,
        #     'cigarette_lighter_out': self.cigarette_lighter_out,
        #     'cassette_cd_out': self.cassette_cd_out,
        #     'ac_pots_out': self.ac_pots_out,
        #     'sun_visors_out': self.sun_visors_out,
        #     'inside_mirror_out': self.inside_mirror_out,
        #     'sun_roof_out': self.sun_roof_out,
        #     'window_buttons_out': self.window_buttons_out,
        #     'outside_mirror_button_out': self.outside_mirror_button_out,
        #     'antenna_out': self.antenna_out,
        #     'wipers_out': self.wipers_out,
        #     'hub_caps_out': self.hub_caps_out,
        #     'tyre_check_out': self.tyre_check_out,
        #     'cleanness_out_out': self.cleanness_out_out,
        #     'cleanness_in_out': self.cleanness_in_out,
        #     'screwdrivers_in': self.screwdrivers_in,
        #     'jack_hummer_in': self.jack_hummer_in,
        #     'tyre_spanner_in': self.tyre_spanner_in,
        #     'first_aid_in': self.first_aid_in,
        #     'hazard_triangle_in': self.hazard_triangle_in,
        #     'spare_tyre_in': self.spare_tyre_in,
        #     'fire_ext_in': self.fire_ext_in,
        #     'boot_mats_in': self.boot_mats_in,
        #     'license_in': self.license_in,
        #     'cigarette_tray_in': self.cigarette_tray_in,
        #     'cassette_cd_in': self.cassette_cd_in,
        #     'ac_pots_in': self.ac_pots_in,
        #     'sun_visors_in': self.sun_visors_in,
        #     'inside_mirror_in': self.inside_mirror_in,
        #     'sun_roof_in': self.sun_roof_in,
        #     'window_buttons_in': self.window_buttons_in,
        #     'outside_mirror_button_in': self.outside_mirror_button_in,
        #     'antenna_in': self.antenna_in,
        #     'wipers_in': self.wipers_in,
        #     'tyre_check_in': self.tyre_check_in,
        #     'cleanness_out_in': self.cleanness_out_in,
        #     'cleanness_in_in': self.cleanness_in_in,
        #     'check_out_comments': self.check_out_comments,
        #     'check_in_comments': self.check_in_comments,
        #     'damage_charge': self.damage_charge,
        #     'km_included_per_month': self.km_included_per_month,
        #
        # })
        return super(PreLease, self).create(vals_list)

    @api.model
    def get_report_name(self):
        return _("Pre-Lease")


class ShortContract(models.Model):
    _name = 'short.contract'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'Short Term'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="contract_id", string="", required=False, )

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('short.contract') or _('New')
        # self.env['all.args'].create({
        #     'name': self.name,
        #     'customer_id': self.customer_id.id,
        #     'contract_id': self.contract_id.id,
        #     'contact_id': self.contact_id.id,
        #     'vo_id': self.vo_id.id,
        #     'fleet_in': self.fleet_in.id,
        #     'fleet_out': self.fleet_out.id,
        #     'user_id': self.user_id,
        #     'license_number': self.license_number,
        #     'license_issue_place': self.license_issue_place,
        #     'vehicle_id': self.vehicle_id.id,
        #     'vin_number': self.vin_number,
        #     'vehicle_model': self.vehicle_model.id,
        #     'vehicle_color': self.vehicle_color,
        #     'engine_number': self.engine_number,
        #     'child_ids': self.child_ids.ids,
        #     'owner_name': self.owner_name,
        #     'user_name': self.user_name.id,
        #     'email': self.email,
        #     'id_expiry_date': self.id_expiry_date,
        #     'license_expiry_date': self.license_expiry_date,
        #     'extra_km_rate': self.extra_km_rate,
        #     'car_out': self.car_out.id,
        #     'car_in': self.car_in.id,
        #     'date_out': self.date_out,
        #     'time_out': self.time_out,
        #     'km_reading_out': self.km_reading_out,
        #     'fuel_out': self.fuel_out,
        #     'date_in': self.date_in,
        #     'time_in': self.time_in,
        #     'km_reading_in': self.km_reading_in,
        #     'fuel_in': self.fuel_in,
        #     'screwdrivers_out': self.screwdrivers_out,
        #     'jack_hummer_out': self.jack_hummer_out,
        #     'tyre_spanner_out': self.tyre_spanner_out,
        #     'first_aid_out': self.first_aid_out,
        #     'hazard_triangle_out': self.hazard_triangle_out,
        #     'spare_tyre_out': self.spare_tyre_out,
        #     'fire_ext_out': self.fire_ext_out,
        #     'boot_mats_out': self.boot_mats_out,
        #     'license_out': self.license_out,
        #     'cigarette_tray_out': self.cigarette_tray_out,
        #     'cigarette_lighter_out': self.cigarette_lighter_out,
        #     'cassette_cd_out': self.cassette_cd_out,
        #     'ac_pots_out': self.ac_pots_out,
        #     'sun_visors_out': self.sun_visors_out,
        #     'inside_mirror_out': self.inside_mirror_out,
        #     'sun_roof_out': self.sun_roof_out,
        #     'window_buttons_out': self.window_buttons_out,
        #     'outside_mirror_button_out': self.outside_mirror_button_out,
        #     'antenna_out': self.antenna_out,
        #     'wipers_out': self.wipers_out,
        #     'hub_caps_out': self.hub_caps_out,
        #     'tyre_check_out': self.tyre_check_out,
        #     'cleanness_out_out': self.cleanness_out_out,
        #     'cleanness_in_out': self.cleanness_in_out,
        #     'screwdrivers_in': self.screwdrivers_in,
        #     'jack_hummer_in': self.jack_hummer_in,
        #     'tyre_spanner_in': self.tyre_spanner_in,
        #     'first_aid_in': self.first_aid_in,
        #     'hazard_triangle_in': self.hazard_triangle_in,
        #     'spare_tyre_in': self.spare_tyre_in,
        #     'fire_ext_in': self.fire_ext_in,
        #     'boot_mats_in': self.boot_mats_in,
        #     'license_in': self.license_in,
        #     'cigarette_tray_in': self.cigarette_tray_in,
        #     'cassette_cd_in': self.cassette_cd_in,
        #     'ac_pots_in': self.ac_pots_in,
        #     'sun_visors_in': self.sun_visors_in,
        #     'inside_mirror_in': self.inside_mirror_in,
        #     'sun_roof_in': self.sun_roof_in,
        #     'window_buttons_in': self.window_buttons_in,
        #     'outside_mirror_button_in': self.outside_mirror_button_in,
        #     'antenna_in': self.antenna_in,
        #     'wipers_in': self.wipers_in,
        #     'tyre_check_in': self.tyre_check_in,
        #     'cleanness_out_in': self.cleanness_out_in,
        #     'cleanness_in_in': self.cleanness_in_in,
        #     'check_out_comments': self.check_out_comments,
        #     'check_in_comments': self.check_in_comments,
        #     'damage_charge': self.damage_charge,
        #     'km_included_per_month': self.km_included_per_month,
        #
        # })
        return super(ShortContract, self).create(vals_list)

    @api.model
    def get_report_name(self):
        return _("Short Term")


class OutSource(models.Model):
    _name = 'out.source'
    _inherit = 'car.rental.agreement'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    invoice_start_date = fields.Date(string="Invoice Start Date ", required=False, )
    initial_km = fields.Float(string="Initial KM", required=False, )
    car_move_ids = fields.One2many(comodel_name="car.move", inverse_name="out_source_id", string="", required=False, )
    is_updated = fields.Boolean()

    def update_vo_action(self):
        value = {
            'name': '/',
            'fleet_licence_plate_id': self.vehicle_id.id,
            'initial_km': self.initial_km,
            'invoice_start_date': self.invoice_start_date,
            'outsource_serial': self.name,
            'vehicle_order_id': self.vo_id.id,
        }
        # self.vo_id.model_id = self.vehicle_id.model_id.id
        self.vo_id.vehicle_car_ids = [(0, 0, value)]
        self.is_updated = True

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('out.source') or _('New')
        return super(OutSource, self).create(vals_list)

    # def write(self, vals):
    #     res= super(OutSource, self).write(vals)
    #     self.env['all.args'].create({
    #         'name': self.name,
    #         'customer_id': self.customer_id.id,
    #         'contract_id': self.contract_id.id,
    #         'contact_id': self.contact_id.id,
    #         'vo_id': self.vo_id.id,
    #         'fleet_in': self.fleet_in.id,
    #         'fleet_out': self.fleet_out.id,
    #         'user_id': self.user_id,
    #         'license_number': self.license_number,
    #         'license_issue_place': self.license_issue_place,
    #         'vehicle_id': self.vehicle_id.id,
    #         'vin_number': self.vin_number,
    #         'vehicle_model': self.vehicle_model.id,
    #         'vehicle_color': self.vehicle_color,
    #         'engine_number': self.engine_number,
    #         'child_ids': self.child_ids.ids,
    #         'owner_name': self.owner_name,
    #         'user_name': self.user_name.id,
    #         'email': self.email,
    #         'id_expiry_date': self.id_expiry_date,
    #         'license_expiry_date': self.license_expiry_date,
    #         'extra_km_rate': self.extra_km_rate,
    #         'car_out': self.car_out.id,
    #         'car_in': self.car_in.id,
    #         'date_out': self.date_out,
    #         'time_out': self.time_out,
    #         'km_reading_out': self.km_reading_out,
    #         'fuel_out': self.fuel_out,
    #         'date_in': self.date_in,
    #         'time_in': self.time_in,
    #         'km_reading_in': self.km_reading_in,
    #         'fuel_in': self.fuel_in,
    #         'screwdrivers_out': self.screwdrivers_out,
    #         'jack_hummer_out': self.jack_hummer_out,
    #         'tyre_spanner_out': self.tyre_spanner_out,
    #         'first_aid_out': self.first_aid_out,
    #         'hazard_triangle_out': self.hazard_triangle_out,
    #         'spare_tyre_out': self.spare_tyre_out,
    #         'fire_ext_out': self.fire_ext_out,
    #         'boot_mats_out': self.boot_mats_out,
    #         'license_out': self.license_out,
    #         'cigarette_tray_out': self.cigarette_tray_out,
    #         'cigarette_lighter_out': self.cigarette_lighter_out,
    #         'cassette_cd_out': self.cassette_cd_out,
    #         'ac_pots_out': self.ac_pots_out,
    #         'sun_visors_out': self.sun_visors_out,
    #         'inside_mirror_out': self.inside_mirror_out,
    #         'sun_roof_out': self.sun_roof_out,
    #         'window_buttons_out': self.window_buttons_out,
    #         'outside_mirror_button_out': self.outside_mirror_button_out,
    #         'antenna_out': self.antenna_out,
    #         'wipers_out': self.wipers_out,
    #         'hub_caps_out': self.hub_caps_out,
    #         'tyre_check_out': self.tyre_check_out,
    #         'cleanness_out_out': self.cleanness_out_out,
    #         'cleanness_in_out': self.cleanness_in_out,
    #         'screwdrivers_in': self.screwdrivers_in,
    #         'jack_hummer_in': self.jack_hummer_in,
    #         'tyre_spanner_in': self.tyre_spanner_in,
    #         'first_aid_in': self.first_aid_in,
    #         'hazard_triangle_in': self.hazard_triangle_in,
    #         'spare_tyre_in': self.spare_tyre_in,
    #         'fire_ext_in': self.fire_ext_in,
    #         'boot_mats_in': self.boot_mats_in,
    #         'license_in': self.license_in,
    #         'cigarette_tray_in': self.cigarette_tray_in,
    #         'cassette_cd_in': self.cassette_cd_in,
    #         'ac_pots_in': self.ac_pots_in,
    #         'sun_visors_in': self.sun_visors_in,
    #         'inside_mirror_in': self.inside_mirror_in,
    #         'sun_roof_in': self.sun_roof_in,
    #         'window_buttons_in': self.window_buttons_in,
    #         'outside_mirror_button_in': self.outside_mirror_button_in,
    #         'antenna_in': self.antenna_in,
    #         'wipers_in': self.wipers_in,
    #         'tyre_check_in': self.tyre_check_in,
    #         'cleanness_out_in': self.cleanness_out_in,
    #         'cleanness_in_in': self.cleanness_in_in,
    #         'check_out_comments': self.check_out_comments,
    #         'check_in_comments': self.check_in_comments,
    #         'damage_charge': self.damage_charge,
    #         'km_included_per_month': self.km_included_per_month,
    #
    #     })
    #     return res

    @api.model
    def get_report_name(self):
        return _("Out Source")


class VehicleRestitution(models.Model):
    _name = 'vehicle.restitution'
    _rec_name = 'name'
    _description = 'all arguments'

    name = fields.Char('seq', required=True, default=_('New'), copy=False)
    customer_id = fields.Many2one(comodel_name="res.partner", string="", required=False, )
    contact = fields.Many2one(comodel_name="res.partner", string="", required=False, )
    plate_no = fields.Integer(string="Plate Number", required=False, )
    vehicle_id = fields.Many2one(comodel_name="vehicle.order", string="", required=False, )
    vo_start_date = fields.Date()
    vo_end_date = fields.Date()
    mla_id = fields.Many2one(comodel_name="mla.data")
    mla_start_date = fields.Date()
    mla_end_date = fields.Date()
    fleet_in = fields.Many2one(comodel_name="stock.move", string="", required=False, )
    fleet_out = fields.Many2one(comodel_name="stock.move", string="", required=False, )
    state = fields.Selection(
        selection=[('draft', 'draft'), ('sent', 'Request Sent'), ('inprogress', 'In Progress'),
                   ('renew', 'To Renew'), ('closed', 'Closed')], required=False, default="draft")
    start_date = fields.Date()
    end_date = fields.Date()

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('vehicle.restitution') or _('New')

    # def write(self, vals):
    #     res= super(VehicleRestitution, self).write(vals)
    #     self.env['all.args'].create({
    #         'name': self.name,
    #         'customer_id': self.customer_id.id,
    #         'contract_id': self.contract_id.id,
    #         'contact_id': self.contact_id.id,
    #         'vo_id': self.vo_id.id,
    #         'fleet_in': self.fleet_in.id,
    #         'fleet_out': self.fleet_out.id,
    #         'user_id': self.user_id,
    #         'license_number': self.license_number,
    #         'license_issue_place': self.license_issue_place,
    #         'vehicle_id': self.vehicle_id.id,
    #         'vin_number': self.vin_number,
    #         'vehicle_model': self.vehicle_model.id,
    #         'vehicle_color': self.vehicle_color,
    #         'engine_number': self.engine_number,
    #         'child_ids': self.child_ids.ids,
    #         'owner_name': self.owner_name,
    #         'user_name': self.user_name.id,
    #         'email': self.email,
    #         'id_expiry_date': self.id_expiry_date,
    #         'license_expiry_date': self.license_expiry_date,
    #         'extra_km_rate': self.extra_km_rate,
    #         'car_out': self.car_out.id,
    #         'car_in': self.car_in.id,
    #         'date_out': self.date_out,
    #         'time_out': self.time_out,
    #         'km_reading_out': self.km_reading_out,
    #         'fuel_out': self.fuel_out,
    #         'date_in': self.date_in,
    #         'time_in': self.time_in,
    #         'km_reading_in': self.km_reading_in,
    #         'fuel_in': self.fuel_in,
    #         'screwdrivers_out': self.screwdrivers_out,
    #         'jack_hummer_out': self.jack_hummer_out,
    #         'tyre_spanner_out': self.tyre_spanner_out,
    #         'first_aid_out': self.first_aid_out,
    #         'hazard_triangle_out': self.hazard_triangle_out,
    #         'spare_tyre_out': self.spare_tyre_out,
    #         'fire_ext_out': self.fire_ext_out,
    #         'boot_mats_out': self.boot_mats_out,
    #         'license_out': self.license_out,
    #         'cigarette_tray_out': self.cigarette_tray_out,
    #         'cigarette_lighter_out': self.cigarette_lighter_out,
    #         'cassette_cd_out': self.cassette_cd_out,
    #         'ac_pots_out': self.ac_pots_out,
    #         'sun_visors_out': self.sun_visors_out,
    #         'inside_mirror_out': self.inside_mirror_out,
    #         'sun_roof_out': self.sun_roof_out,
    #         'window_buttons_out': self.window_buttons_out,
    #         'outside_mirror_button_out': self.outside_mirror_button_out,
    #         'antenna_out': self.antenna_out,
    #         'wipers_out': self.wipers_out,
    #         'hub_caps_out': self.hub_caps_out,
    #         'tyre_check_out': self.tyre_check_out,
    #         'cleanness_out_out': self.cleanness_out_out,
    #         'cleanness_in_out': self.cleanness_in_out,
    #         'screwdrivers_in': self.screwdrivers_in,
    #         'jack_hummer_in': self.jack_hummer_in,
    #         'tyre_spanner_in': self.tyre_spanner_in,
    #         'first_aid_in': self.first_aid_in,
    #         'hazard_triangle_in': self.hazard_triangle_in,
    #         'spare_tyre_in': self.spare_tyre_in,
    #         'fire_ext_in': self.fire_ext_in,
    #         'boot_mats_in': self.boot_mats_in,
    #         'license_in': self.license_in,
    #         'cigarette_tray_in': self.cigarette_tray_in,
    #         'cassette_cd_in': self.cassette_cd_in,
    #         'ac_pots_in': self.ac_pots_in,
    #         'sun_visors_in': self.sun_visors_in,
    #         'inside_mirror_in': self.inside_mirror_in,
    #         'sun_roof_in': self.sun_roof_in,
    #         'window_buttons_in': self.window_buttons_in,
    #         'outside_mirror_button_in': self.outside_mirror_button_in,
    #         'antenna_in': self.antenna_in,
    #         'wipers_in': self.wipers_in,
    #         'tyre_check_in': self.tyre_check_in,
    #         'cleanness_out_in': self.cleanness_out_in,
    #         'cleanness_in_in': self.cleanness_in_in,
    #         'check_out_comments': self.check_out_comments,
    #         'check_in_comments': self.check_in_comments,
    #         'damage_charge': self.damage_charge,
    #         'km_included_per_month': self.km_included_per_month,
    #
    #     })
    #     return res
