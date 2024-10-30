from odoo import models, fields, api


class VehicleInsurance(models.Model):
    _inherit = 'vehicle.insurance'

    model_m_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Models",)
    model_search = fields.Char(compute='get_model_search_name', string="Model Search",store=True)
    make_m_id = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturers",)
    category_m_id = fields.Many2one("fleet.vehicle.model.category", string="Category",)
    year_id = fields.Many2one("fleet.vehicle.model.year", string="Year",)
    pending_delivery_id = fields.Many2one('pending.delivery', string='Pending Delivery',)
    # insurance_no = fields.Integer('Insurance No.', tracking=True,)
    insurance_no = fields.Char('Insurance No.', tracking=True,)
    insurance_year = fields.Integer('Insurance Years', tracking=True, default=1,)
    from_pending_delivery = fields.Boolean(string="From Pending Delivery", copy=False,)

    # @api.depends('vehicle_id')
    # def get_model_search_name(self):
    #     print(f'in get_model_search_name')
    #     for rec in self:
    #         if rec.vehicle_id:
    #             if rec.vehicle_id.model_id:
    #                 if rec.vehicle_id.model_id.brand_id:
    #                     rec.model_search = rec.vehicle_id.model_id.brand_id.name+ '/'+rec.vehicle_id.model_id.name
    #                 elif not rec.vehicle_id.model_id.brand_id:
    #                     rec.model_search = rec.vehicle_id.model_id.name
    #                 else:
    #                     rec.model_search = None
    #         else:
    #             rec.model_search = None

    @api.depends('model_m_id')
    def get_model_search_name(self):
        print(f'in get_model_search_name')
        for rec in self:
            if rec.model_m_id:
                rec.model_search = rec.model_m_id.brand_id.name + '/' + rec.model_m_id.name
            else:
                rec.model_search = None
