from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for pick in self:
            for line in pick.move_ids_without_package:
                if line.odometer_value > 0 and line.lot_ids:
                    for lot in line.lot_ids:
                        odometer_obj = self.env['fleet.cars.odometer.line'].search(
                            [('vehicle_id', '=', lot.vehicle_id.id)])
                        for odo in odometer_obj:
                            odo.value = line.odometer_value
                        vehicle_odometer_obj = self.env['fleet.vehicle.odometer'].create(
                            {'date':  fields.Datetime.now(), 'driver_id': lot.vehicle_id.driver_id.id,
                             'vehicle_id': lot.vehicle_id.id, 'value': line.odometer_value, 'unit': 'km'})

        return super(StockPicking, self).button_validate()


class StockMove(models.Model):
    _inherit = 'stock.move'

    odometer_value = fields.Float('Odometer Value')
