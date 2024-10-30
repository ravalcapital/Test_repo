# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class VehicleLicense(models.Model):
    _name = "vehicle.license"
    _description = "Vehicle License"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_search_name = fields.Char(compute="_compute_vehicle_name", store=True)
    car_plate_no = fields.Char(string="Car Plate No.")
    license_years = fields.Char(string="License Years")
    license_start_date = fields.Date(string="License Start Date", tracking=True)
    # license_probation_date = fields.Date(string="License Probation Date", tracking=True )
    license_probation_date = fields.Date(string="Traffic Inspection Date", tracking=True )
    license_renewal_date = fields.Date(string="License Renewal Date", tracking=True )
    name = fields.Char(string="License Code", required=False,readonly=False )
    pending_delivery_id = fields.Many2one('pending.delivery', string="Pending Delivery")
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Car", required=False, )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'running'),
        ('expired', 'Expired'),
    ], default='draft',track_visibility='onchange')

    # @api.depends('model_id.brand_id.name', 'model_id.name', 'license_plate')
    # def _compute_vehicle_name(self):
    #     for record in self:
    #         record.name = (record.model_id.brand_id.name or '') + '/' + (record.model_id.name or '') + '/' + (record.license_plate or _('No Plate'))
    @api.depends('vehicle_id')
    def _compute_vehicle_name(self):
        for record in self:
            # record.name = (record.model_id.brand_id.name or '') + '/' + (record.model_id.name or '') + '/' + (record.license_plate or _('No Plate'))
            record.vehicle_search_name = (record.vehicle_id.model_id.brand_id.name or '') + '/' + (record.vehicle_id.model_id.name or '') + '/' + (record.vehicle_id.license_plate or _('No Plate'))

    # tracking = True
    # def message_click(self):
    #     print(f'in message_click')
    #     for rec in self:
    #         msg = 'hello from chatttttttttttt'
    #         rec.message_post(body=msg )
        # track_visibility='onchange')
    # change_time = fields.Datetime(string= 'Change Time',)
    # user_id = fields.Many2one('res.users', string="Current User", default=lambda self: self.env.user)
    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.license')
    #     return super(VehicleLicense, self).create(vals)
    # default=lambda self: fields.Datetime.now()

    # @api.onchange('state')
    # def onchange_state(self):
    #     print(f'in _onchange_state ')
    #     # for rec in self:
    #     msg = 'hello from chatttttttttttt222222'
    #     user_id = self.env.user
    #     change_time = fields.Datetime.now()
    #     # body = 'User : ' + user_id.name + ' Changed the WorkFlow to ' + self.state + '' + ' on '+str(change_time)
    #     body = 'User :  Changed the WorkFlow to '
    #     print(f'_onchange_state - body :{body}')
    #     self.message_post(body=body,)
    #     # rec.message_notify(body=body,)
    #     # rec.message_notify(
    #     #     subject=body,
    #     #     body=body,
    #     #     partner_ids=user_id.partner_id.ids,
    #     #     record_name=rec.display_name,
    #     #     email_layout_xmlid='mail.mail_notification_light',
    #     #     model_description=body,
    #     # )
    #     return self.message_post(body=body)

    # message_notify
    # author_id = user_id.partner_id.id

    # def _post_author(self):
    #     user_id = self.env.user
    #     return user_id
    # @api.returns('mail.message', lambda value: value.id)
    # def message_post(self, **kwargs):
    #     return self._post_author().message_post(**kwargs)
            # self.message_post(body=body,)
            # self.message_notify(body=body,)
            # self.message_notify(
            #     body=body,
            #     partner_ids=[self.user_id.partner_id.id],
            #     subtype_xmlid='mail.mt_comment',
            #     email_layout_xmlid='mail.mail_notification_light',
            # )
            # return self.message_post(body=body)
        # self.sudo().message_post(body=body, author_id=user_id.partner_id.id,message_type='comment',
        #                 subtype_xmlid='mail.mt_note')
# _message_post_after_hook
# message_post_with_view
# _notify_message_notification_update
# message_notify