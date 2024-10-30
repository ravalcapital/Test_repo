# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    # archive_date = fields.Date(default=fields.Date.context_today, string="Archive Date")
    archive_date = fields.Date(string="Archive Date")

    def write(self, vals):
        if 'active' in vals and not vals['active']:
            for rec in self:
                if 'archive_date' in vals or rec.archive_date:
                    archive_date ='archive_date' if 'archive_date' in vals else rec.archive_date
                    if rec.vo_id and archive_date:
                        if rec.vo_id.vehicle_payments:
                            vehicle_payments_invoices = rec.vo_id.vehicle_payments.filtered(lambda p: p.date_from <= archive_date and p.date_to >= archive_date and p.vehicle_licence.id == rec.id )
                            vehicle_payments_invoices_to_delete = rec.vo_id.vehicle_payments.filtered(lambda p: p.date_from > archive_date and p.date_to > archive_date and p.vehicle_licence.id == rec.id )
                            if vehicle_payments_invoices:
                                vehicle_payments_invoices.date_to = archive_date
                            if vehicle_payments_invoices_to_delete:
                                vehicle_payments_invoices_to_delete.unlink()

                        if rec.vo_id.millage_car_details_ids:
                            vehicle_millage_invoices = rec.vo_id.millage_car_details_ids.filtered(lambda p: p.date_from <= archive_date and p.date_to >= archive_date and p.vehicle_licence.id == rec.id )
                            vehicle_millage_invoices_to_delete = rec.vo_id.millage_car_details_ids.filtered(lambda p: p.date_from > archive_date and p.date_to > archive_date and p.vehicle_licence.id == rec.id )

                            if vehicle_millage_invoices:
                                vehicle_millage_invoices.date_to = archive_date
                            if vehicle_millage_invoices_to_delete:
                                vehicle_millage_invoices_to_delete.unlink()
                    elif rec.vo_id and not archive_date:
                        raise UserError('You Must Set Archive Date..')

        res = super(FleetVehicle, self).write(vals)
        return res
