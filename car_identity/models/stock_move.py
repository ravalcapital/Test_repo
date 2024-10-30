from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    car_identity_ids = fields.Many2many('car.identity', string='Car Identity')

    @api.onchange('lot_ids')
    def _onchange_lot_ids(self):
        lot_list = []
        if self.lot_ids:
            for lot_id in self.lot_ids:
                if lot_id.car_identity_id:
                   lot_list.append(lot_id.car_identity_id.id)
                if lot_id.vehicle_id:
                    if lot_id.vehicle_id.car_identity_id:
                        lot_list.append(lot_id.vehicle_id.car_identity_id.id)
                    self.model_m_id = lot_id.vehicle_id.model_id.id
                    self.year_id = lot_id.vehicle_id.year_id.id
                    if lot_id.vehicle_id.model_id:
                        self.make_m_id = lot_id.vehicle_id.model_id.brand_id.id
                        self.category_m_id = lot_id.vehicle_id.model_id.category_id.id
                        self.vehicle_grade_id = lot_id.vehicle_id.vehicle_grade_id.id
                    else:
                        self.make_m_id = False
                        self.category_m_id = False
                        self.vehicle_grade_id = False
                    # self.color_id = self.lot_id.vehicle_id.model_id.id
                else:
                    self.model_m_id = False
                    self.year_id = False
                    self.make_m_id = False
                    self.category_m_id = False
                    self.vehicle_grade_id = False
        else:
            self.model_m_id = False
            self.year_id = False
            self.make_m_id = False
            self.category_m_id = False
        if self.lot_ids and not self.car_identity_ids:
            self.car_identity_ids = [(6, 0, set(lot_list))]
        return super(StockMove, self)._onchange_lot_ids()

    # @api.depends('lot_ids')
    # def get_lot_car_identity_id(self):
    #     for rec in self:
    #         lot_list = []
    #         for lot in rec.lot_ids:
    #             lot_list.append(lot.car_identity_id.id)
    #         rec.car_identity_ids = [(6, 0, lot_list)]


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # car_identity_id = fields.Many2one('car.identity', string='Car Identity')

    @api.onchange('lot_name', 'lot_id')
    def _onchange_serial_number(self):
        if self.lot_id and self.lot_id.vehicle_id:
            self.model_m_id = self.lot_id.vehicle_id.model_id.id
            self.year_id = self.lot_id.vehicle_id.year_id.id
            if self.lot_id.vehicle_id.model_id:
                self.make_m_id = self.lot_id.vehicle_id.model_id.brand_id.id
                self.category_m_id = self.lot_id.vehicle_id.model_id.category_id.id
                self.vehicle_grade_id = self.lot_id.vehicle_id.vehicle_grade_id.id
            else:
                self.make_m_id = False
                self.category_m_id = False
                self.vehicle_grade_id = False
            # self.color_id = self.lot_id.vehicle_id.model_id.id
        else:
            self.model_m_id = False
            self.year_id = False
            self.make_m_id = False
            self.category_m_id = False
            self.vehicle_grade_id = False

        return super(StockMoveLine, self)._onchange_serial_number()

#     @api.onchange('move_id.car_identity_ids')
#     def _onchange_car_identity_ids(self):
#         if self.move_id.car_identity_ids and not self.car_identity_id:
#             car_list = []
#             for car in self.move_id.car_identity_ids:
#                 car_list.append(car.id)
#             if len(car_list) > 0:
#                self.car_identity_id = car_list[0]
#         return super(StockMoveLine, self)._onchange_serial_number()
#
