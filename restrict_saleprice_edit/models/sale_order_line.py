

from odoo import models, api, _
from odoo.exceptions import UserError


class SaleOrderline(models.Model):
    _inherit = "sale.order.line"


