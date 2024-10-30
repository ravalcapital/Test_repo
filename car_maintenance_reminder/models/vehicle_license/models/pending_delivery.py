# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PendingDelivery(models.Model):
    _inherit = 'pending.delivery'

    vehicle_license_ids = fields.One2many('vehicle.license', 'pending_delivery_id', string="Vehicle License", ondelete='restrict')
    vehicle_license_count = fields.Integer(compute="compute_vehicle_license_count")

    @api.depends('vehicle_license_ids')
    def compute_vehicle_license_count(self):
        for rec in self:
            rec.vehicle_license_count = len(rec.vehicle_license_ids)

    def action_view_vehicle_license(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle License'),
            'res_model': 'vehicle.license',
            'view_mode': 'tree,form',
            "context": {"pending_delivery_id": self.id,
                        "default_pending_delivery_id": self.id,
                        "default_car_plate_no": self.car_plate_no,
                        "default_license_years": self.license_year,
                        "default_license_start_date": self.license_start_date,
                        "default_license_probation_date": self.license_probation_period,
                        "default_license_renewal_date": self.license_renewal_date,
                        },
            'domain': [('id', 'in', self.mapped('vehicle_license_ids').ids)],
        }

    def action_create_vehicle_license(self):
        vehicle_license_ids = self.mapped('vehicle_license_ids')
        list_view = self.env.ref('vehicle_license.vehicle_license_tree_view')
        form_view = self.env.ref('vehicle_license.vehicle_license_form_view')
        if len(vehicle_license_ids) <= 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Vehicle License'),
                'res_model': 'vehicle.license',
                'view_mode': 'form',
                'views': [[form_view.id, 'form']],
                'context': {"default_pending_delivery_id": self.id,
                            "default_car_plate_no": self.car_plate_no,
                            "default_license_years": self.license_year,
                            "default_license_start_date": self.license_start_date,
                            "default_license_probation_date": self.license_probation_period,
                            "default_license_renewal_date": self.license_renewal_date,
                            "default_name": self.license_code,
                            },
                'res_id': vehicle_license_ids.id,

            }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vehicle License'),
            'res_model': 'vehicle.license',
            'view_mode': 'list,form',
            'views': [[list_view.id, 'list'], [form_view.id, 'form']],
            'context': {"default_pending_delivery_id": self.id,
                            "default_car_plate_no": self.car_plate_no,
                            "default_license_years": self.license_year,
                            "default_license_start_date": self.license_start_date,
                            "default_license_probation_date": self.license_probation_period,
                            "default_license_renewal_date": self.license_renewal_date,},
            'domain': [('id', 'in', vehicle_license_ids.ids)],
        }

