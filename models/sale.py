from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_note = fields.Char(string='Customer Note')