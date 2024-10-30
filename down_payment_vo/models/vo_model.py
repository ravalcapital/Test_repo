from odoo import models, fields, api, _


class ObjectPayment(models.Model):
    _name = 'vo.account.payment.line'

    customer_id = fields.Many2one(comodel_name="res.partner")
    vo_id = fields.Many2one(comodel_name="vehicle.order")
    payment_reference = fields.Char(string="", required=False, )
    memo = fields.Char(string="", required=False)
    amount = fields.Float(string="", required=False, )
    defa = fields.Float(string="", required=False, )
    payment_date = fields.Date(string="", required=False, )
    payment_id = fields.Many2one(comodel_name="account.payment", string="", required=False, )
    state = fields.Selection(related='payment_id.state')
    journal_id = fields.Many2one(comodel_name="account.journal", string="", required=False, )
    is_created = fields.Boolean(default=False)

    @api.onchange('defa')
    def get_default_val(self):
        print(self.vo_id)
        print('onchangeeeeeee')
        self.customer_id = self.vo_id.customer_id.id
        self.memo = '[MLA:%s,%s]' % (self.vo_id.mla_id.name or '', self.vo_id.name or '')
        self.amount = self.vo_id.unit_price * self.vo_id.no_Vehicles
        self.payment_date = fields.date.today()

    def button_create_payment(self):
        payment_method = self.env['account.payment.method'].search(
            [('code', '=', 'manual'), ('payment_type', '=', 'outbound')], limit=1)
        if payment_method:
            method = self.env['account.payment.method.line'].search(
                [('payment_method_id', '=', payment_method.id), ('code', '=', 'manual')], limit=1)
        vals = {
            'payment_type': 'outbound',
            'amount': self.amount,
            'date': self.payment_date,
            'ref': self.memo,
            'vo_id': self.vo_id.id,
            'mla_id': self.vo_id.mla_id.id,
            'journal_id': self.journal_id.id,
            'state': 'draft',
            'vo_line_id': self.id,
            'partner_id': self.customer_id.id,
            'payment_method_line_id': method.id

        }
        payments = self.env['account.payment'].search([], limit=1)
        print(payments.payment_method_line_id)
        payment = self.env['account.payment'].create(vals)
        self.payment_id = payment.id

        self.is_created = True
        # self.write({
        #     'payment_reference':
        # })


class VoInherit(models.Model):
    _inherit = 'vehicle.order'

    payment_ids = fields.One2many(comodel_name="vo.account.payment.line", inverse_name="vo_id")
    payment_compute_ids = fields.Many2many(comodel_name="account.payment", compute="get_payment_ids")
    count = fields.Integer(string="", required=False,compute="get_payment_ids")

    @api.depends('payment_ids.payment_id')
    def get_payment_ids(self):
        for rec in self:
            payments = self.env['account.payment'].search([('vo_id', '=', self.id)])
            rec.payment_compute_ids = [(6, 0, payments.ids)]
            rec.count = len(payments)

    def get_payments_button(self):
        self.ensure_one()
        return {
            'name': _('Down Payments'),
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', self.payment_compute_ids.ids)],
            'target': 'current',
        }
