from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_note = fields.Char(string='Customer Note')

    # Banking details for custom quotation
    bank_name = fields.Char(string='Bank Name')
    account_number = fields.Char(string='Account Number')
    ifsc_code = fields.Char(string='IFSC Code')
    branch_name = fields.Char(string='Branch Name')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one(comodel_name='product.brand', string='Product Brand')