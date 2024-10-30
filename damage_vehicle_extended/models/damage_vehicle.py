from odoo import models, fields, api


class DamageVehicle(models.Model):
    _inherit = 'damage.vehicle'

    service_center_id = fields.Many2one(comodel_name="res.partner", string=" Service Center", required=False, )
    # default_customer_journal = fields.Many2one('account.journal',string='Default Customer Journal',domain="[('type', '=', 'sale'))]")
    # default_vendor_journal = fields.Many2one('account.journal',string='Default Vendor Journal', domain="[('type', '=', 'purchase'))]")

    default_customer_journal = fields.Many2one('account.journal',string='Default Customer Journal',domain=[('type', '=','sale')])
    default_vendor_journal = fields.Many2one('account.journal',string='Default Vendor Journal', domain=[('type', '=','purchase')])


    state = fields.Selection([
        ('draft', 'Draft'),
        ('billing', 'Billing'),
        ('done', 'Done')], string='Status',
        copy=False, default='draft', required=True, tracking=True)
    # user_id = fields.Many2one('res.users')
    # show_buttons = fields.Boolean(related='user_id.show_buttons')

    def done_button(self):
        self.write({
            'state': 'done'
        })

    def confirm_action(self):
        res = super(DamageVehicle, self).confirm_action()
        self.state = 'billing'
        return res

    def create_invoice_customer(self):
        form = self.env.ref('account.view_move_form')
        line = self.damage_vehicle_line_ids[0] if len(self.damage_vehicle_line_ids) > 0 else False
        # journal_claim = self.env['account.journal'].search([('code', '=', 'claim')])
        # print(f'in create_invoice_customer -journal_claim :{journal_claim} ')

        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': form.id,
            'res_model': 'account.move',
            'target': 'current',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_mla_id': line.mla_id.id if line else False,
                'default_vo_id': line.vo_id.id if line else False,
                'default_serial_damage_id': self.id,
                'default_move_type': 'out_invoice',
                # 'default_journal_id': journal_claim.id if journal_claim else False,
                'default_journal_id': self.default_customer_journal.id if self.default_customer_journal else False,

            }
        }

    def create_bill_service_center(self):
        form = self.env.ref('account.view_move_form')
        line = self.damage_vehicle_line_ids[0] if len(self.damage_vehicle_line_ids) > 0 else False
        journal_claim = self.env['account.journal'].search([('code', '=', 'claim')])
        print(f'in create_bill_service_center -journal_claim :{journal_claim} ')
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': form.id,
            'res_model': 'account.move',
            'target': 'current',
            'context': {
                'default_partner_id': self.service_center_id.id,
                'default_move_type': 'in_invoice',
                'default_serial_damage_id': self.id,
                'default_mla_id': line.mla_id.id if line else False,
                'default_vo_id': line.vo_id.id if line else False,
                # 'default_journal_id': journal_claim.id if journal_claim else False,
                'default_journal_id': self.default_vendor_journal.id if self.default_vendor_journal else False,

            }
        }

    def create_invoice_insurance_company(self):
        form = self.env.ref('account.view_move_form')
        line = self.damage_vehicle_line_ids[0] if len(self.damage_vehicle_line_ids) > 0 else False
        journal_claim=self.env['account.journal'].search([('code','=','claim')])
        print(f'in create_invoice_insurance_company -journal_claim :{journal_claim} ')

        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': form.id,
            'res_model': 'account.move',
            'target': 'current',
            'context': {
                'default_partner_id': self.insurance_company_id.id,
                'default_move_type': 'out_invoice',
                'default_serial_damage_id': self.id,
                'default_mla_id': line.mla_id.id if line else False,
                'default_vo_id': line.vo_id.id if line else False,
                # 'default_journal_id': journal_claim.id if journal_claim else False,
                'default_journal_id': self.default_customer_journal.id if self.default_customer_journal else False,

            }
        }


class DamageVehicleLine(models.Model):
    _inherit = 'damage.vehicle.line'

    @api.onchange('licence_plate')
    def get_product_from_plate(self):
        for record in self:
            record.product_id = record.licence_plate.product_id.id
            record.mla_id = record.licence_plate.vehicle_id.mla_id.id
            record.vo_id = record.licence_plate.vehicle_id.vo_id.id
