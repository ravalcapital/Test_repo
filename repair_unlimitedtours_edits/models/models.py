from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EmployeeDefault(models.Model):
    _name = 'employee.default'
    # _rec_name = 'maintenance_engineer_id'

    maintenance_engineer_id = fields.Many2one(comodel_name="hr.employee", string="Maintenance Engineer ",
                                              required=False, )
    maintenance_quality_id = fields.Many2one(comodel_name="hr.employee", string="Maintenance & Quality Manager  ",
                                             required=False, )
    maintenance_supervisor_id = fields.Many2one(comodel_name="hr.employee", string=" Maintenance Supervisor ",
                                                required=False, )
    maintenance_supervisor2_id = fields.Many2one(comodel_name="hr.employee", string=" Maintenance Supervisor ",
                                                required=False, )



class Repair(models.Model):
    _inherit = 'repair.order'


    def action_validate(self):
        self.ensure_one()
        if self.filtered(lambda repair: any(op.product_uom_qty < 0 for op in repair.operations)):
            raise UserError(_("You can not enter negative quantities."))
        if self.product_id.type == 'consu':
            return self.action_repair_confirm()

        return self.action_repair_confirm()

    @api.model
    def get_quality_id(self):
        employees = self.env['employee.default'].search([], limit=1)
        return employees.maintenance_quality_id.id

    @api.model
    def get_maintenance_supervisor_id(self):
        employees = self.env['employee.default'].search([], limit=1)
        return employees.maintenance_supervisor_id.id

    api.model

    def get_maintenance_supervisor_id(self):
        employees = self.env['employee.default'].search([], limit=1)
        return employees.maintenance_supervisor_id.id

    def get_maintenance_supervisor2_id(self):
        employees = self.env['employee.default'].search([], limit=1)
        return employees.maintenance_supervisor2_id.id
    @api.model
    def get_maintenance_engineer_id(self):
        employees = self.env['employee.default'].search([], limit=1)
        return employees.maintenance_engineer_id.id

    maintenance_quality_id = fields.Many2one('hr.employee', string="Maintenance & quality Manager",
                                             default=get_quality_id)

    mobile_number = fields.Char(related='partner_id.mobile', string='Mobile Number', readonly=False, )
    maintenance_supervisor_id = fields.Many2one('hr.employee', default=get_maintenance_supervisor_id,
                                                string="Maintenance Supervisor")
    maintenance_supervisor2_id = fields.Many2one('hr.employee', default=get_maintenance_supervisor2_id,
                                                string="Maintenance Supervisor")
    supervisor2_work_email = fields.Char(related='maintenance_supervisor2_id.work_email', store=True)
    supervisor2_mobile_phone = fields.Char(related='maintenance_supervisor2_id.mobile_phone', store=True)



    maintenance_engineer_id = fields.Many2one('hr.employee', default=get_maintenance_engineer_id,
                                              string="Maintenance Engineer")

    partner_id = fields.Many2one(related='vehicle_id.customer_id',
                                 string='Customer', domain="[('id', '=', customer_id)]",
                                 index=True, states={'confirmed': [('readonly', True)]}, check_company=True,
                                 change_default=True,
                                 readonly=0,
                                 help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.')

    invoice_number = fields.Char(string="Invoice Number", required=False, )

    # @api.onchange('plate_lot_id')
    # def get_mla_vo(self):
    #     for rec in self:
    #         fleet = self.env['fleet.vehicle'].search([('lot_id', '=', rec.plate_lot_id.id)], limit=1)
    #         if fleet:
    #             rec.mla_id = fleet.mla_id.id
    #             rec.vo_id = fleet.vo_id.id

    @api.onchange('km_in')
    def get_km_out_default(self):
        for rec in self:
            if rec.km_in:
                rec.km_out = rec.km_in

    custom_repair_type = fields.Selection([
        ('predictive', 'Predictive'),
        ('corrective', 'Corrective'),
        ('both', 'Both'), ('accident', 'Accident')], string='Repair Type',
        copy=False, tracking=True)

    @api.constrains('km_in')
    def check_km_validate(self):
        for rec in self:
            if rec.km_in == 0:
                raise ValidationError(_('please enter KM IN'))
