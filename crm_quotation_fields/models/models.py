from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    option_to_puy = fields.Selection([('operating_lease', 'Operating Lease'), ('lease_to_own', 'Lease to Own')],
                                     string='Leasing Type')
    contract_term = fields.Selection([('long_term', 'Long Term'), ('short_term', 'Short Term')],
                                     string='Contract Term')
    millage_calculation = fields.Selection([('pool', 'Pool'), ('limited_km', 'Limited KM')],
                                           string='Millage Calculation')
    total_pool_millage = fields.Float(string='Total Pool Millage')
    mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", required=False, )


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        action = super().action_new_quotation()
        action['context']['default_option_to_puy'] = self.option_to_puy
        action['context']['default_contract_term'] = self.contract_term
        action['context']['default_millage_calculation'] = self.millage_calculation
        action['context']['default_total_pool_millage'] = self.total_pool_millage
        action['context']['default_mla_id'] = self.mla_id.id
        return action



class VehicleOrder(models.Model):
    _inherit = 'vehicle.order'

    # mla_id = fields.Many2one(comodel_name="mla.data", string="MLA", related="order_id.mla_id", store=True)
    mla_id = fields.Many2one(comodel_name="mla.data", string="MLA",)
    start_date = fields.Date("Start Date", related="mla_id.start_date", store=True)
    end_date = fields.Date("End Date", related="mla_id.end_date", store=True)





