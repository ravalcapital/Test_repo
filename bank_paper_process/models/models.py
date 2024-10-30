from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BankPaperObj(models.Model):
    _name = 'bank.paper'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    @api.onchange('create_uid')
    def _get_company_per_user(self):
        company = self.env.company
        self.company_id = company.id
        print(self.company_id)

    name = fields.Char(string='Number', required=True, store=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'), compute="generate_seq")
    state = fields.Selection(string="",
                             selection=[('draft', 'Draft'), ('inprogress', 'In Progress'), ('approved', 'Approved'),
                                        ('done', 'Done')],
                             default="draft")
    loan_id = fields.Many2one('partner.loan.details')
    company_id = fields.Many2one(comodel_name="res.company")
    vehicle_order = fields.Char(string="", required=False, )
    acceptance_form = fields.Binary()
    attachment_1 = fields.Binary(string='Attachment')
    attachment_2 = fields.Binary(string='Attachment')
    attachment_3 = fields.Binary(string='Attachment')
    date_received_1 = fields.Date(string="Date Received", required=False, )
    date_submitted_1 = fields.Date(string="Date Submitted", required=False, )
    date_approved_1 = fields.Date(string="Date Approved", required=False, )
    date_received_2 = fields.Date(string="Date Received", required=False, )
    date_submitted_2 = fields.Date(string="Date Submitted", required=False, )
    date_approved_2 = fields.Date(string="Date Approved", required=False, )
    date_received_3 = fields.Date(string="Date Received", required=False, )
    date_submitted_3 = fields.Date(string="Date Submitted", required=False, )
    date_approved_3 = fields.Date(string="Date Approved", required=False, )
    vendor_po_id = fields.Many2one(comodel_name="purchase.order")
    pending_delivery_lines = fields.One2many('pending.delivery',
                                             related='vendor_po_id.pending_delivery_ids')
    pending_delivery_lines2 = fields.Many2many('pending.delivery', domain="[('bank_id', '=', bank_id),"
                                                                          "('bank_account_id', '=', bank_account_id),"
                                                                          "('state', '=', 'bank_papers')]")
    pending_delivery_id = fields.Many2one('pending.delivery')
    bank_id = fields.Many2one('res.bank', string="Bank", tracking=True, required=True)
    bank_account_id = fields.Many2one('res.partner.bank', string="Bank Account", tracking=True, required=True)

    @api.depends('state')
    def generate_seq(self):
        for rec in self:
            if rec.state != 'draft' and rec.name == _('New'):
                rec.name = self.env['ir.sequence'].next_by_code('bank.paper') or _('New')

    def button_next_stage(self):
        user = self.env.user
        print(user)

        if user.has_group('bank_paper_process.bank_manager_group'):
            if self.state == 'approved':
                self.state = 'done'

        if user.has_group('bank_paper_process.bank_user_group'):
            if self.state == 'approved':
                raise ValidationError(_('This User not to be allowed to change state to done'))

        if self.state == 'draft':
            self.state = 'inprogress'
        elif self.state == 'inprogress':
            self.state = 'approved'

    def back_stage(self):
        if self.state == 'done':
            self.state = 'approved'
        elif self.state == 'approved':
            self.state = 'inprogress'
        elif self.state == 'inprogress':
            self.state = 'draft'
