from odoo import models, fields, api, _

class RepairOrder(models.Model):
    _inherit = 'repair.order'


    @api.onchange('mla_id','state')
    @api.depends('mla_id','state')
    def get_no_tire_same_mla(self):
        print(f'in get_no_tire_same_mla')
        allno_tire = 0
        # plate_lot_id
        for rec in self:
            if rec.mla_id:
                tire_product = self.env['product.product'].search([('tire', '=', True)])
                for tp in tire_product:
                    print(f'tire_product - tp is :{tp}')
                    all_repaires_tire_product = self.env['repair.fee'].search([('product_id', '=', tp.id)])
                    print(f'all_repaires_tire_product are :{all_repaires_tire_product}- rec .mla_id is :{rec.mla_id}')
                    all_repaires_tire_product_filtered = all_repaires_tire_product.filtered(
                        lambda p: p.repair_id.mla_id.id == rec.mla_id.id and p.repair_id.state == 'done' and p.repair_id.plate_lot_id.id == rec.plate_lot_id.id)
                    print(f'all_repaires_tire_product_filtered :{all_repaires_tire_product_filtered}')
                    if all_repaires_tire_product_filtered:
                        allno_tire += sum(all_repaires_tire_product_filtered.mapped('product_uom_qty'))
                        print(f'allno_tire :{allno_tire}')
            rec.no_tire = allno_tire

    @api.depends('vehicle_id','vehicle_id.mla_id','vehicle_id.mla_id.allowed_no_of_tire','no_tire')
    def get_remaining_tire(self):
        for rec in self:
            if rec.vehicle_id:
                if rec.vehicle_id.mla_id:
                    rec.remaining_tire = rec.mla_id.allowed_no_of_tire - rec.no_tire
                else:
                    rec.remaining_tire
            else:
                rec.remaining_tire


    no_tire = fields.Integer('No Of Tire',readonly=1,compute ='get_no_tire_same_mla',store=True)
    remaining_tire = fields.Integer('Remaining Tire',readonly=1,compute ='get_remaining_tire',store=True)

    # def action_repair_end(self):
    #     print(f'in action_repair_end')
    #     all_no_tire = 0.0
    #     tire_product = self.env['product.product'].search([('tire', '=', True)])
    #     all_repairs_tire_product = self.env['repair.fee'].search([('product_id', '=', tire_product.id)])
    #     print(f'all_repairs_tire_product :{all_repairs_tire_product}')
    #     for rec in self:
    #         all_repairs_tire_product_filtered = all_repairs_tire_product.filtered(
    #             lambda p: p.repair_id.mla_id.id == rec.mla_id.id and p.repair_id.state == 'done' and p.repair_id.plate_lot_id.id == rec.plate_lot_id.id)
    #         if all_repairs_tire_product_filtered:
    #             all_no_tire = sum(all_repairs_tire_product_filtered.mapped('product_uom_qty'))
    #         rec.no_tire = all_no_tire
    #     return super(RepairOrder, self).action_repair_end()

    def action_repair_end(self):
        print(f'in action_repair_end')
        all_no_tire = 0.0
        tire_product = self.env['product.product'].search([('tire', '=', True)])
        for tp in tire_product:
            all_repairs_tire_product = self.env['repair.fee'].search([('product_id', '=', tp.id)])
            print(f'all_repairs_tire_product :{all_repairs_tire_product}')
            for rec in self:
                all_repairs_tire_product_filtered = all_repairs_tire_product.filtered(
                    lambda p: p.repair_id.mla_id.id == rec.mla_id.id and p.repair_id.state == 'done' and p.repair_id.plate_lot_id.id == rec.plate_lot_id.id)
                if all_repairs_tire_product_filtered:
                    all_no_tire += sum(all_repairs_tire_product_filtered.mapped('product_uom_qty'))
                rec.no_tire = all_no_tire
        return super(RepairOrder, self).action_repair_end()