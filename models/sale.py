from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_note = fields.Char(string='Customer Note')

    # Banking details for custom quotation
    bank_name = fields.Char(string='Bank Name')
    account_number = fields.Char(string='Account Number')
    ifsc_code = fields.Char(string='IFSC Code')
    branch_name = fields.Char(string='Branch Name')

    def _prepare_invoice(self):
        """
        Override this method to include banking details when creating an invoice from the sale order.
        """
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'bank_name': self.bank_name,
            'account_number': self.account_number,
            'ifsc_code': self.ifsc_code,
            'branch_name': self.branch_name,
        })
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one(comodel_name='product.brand', string='Product Brand')

    def _prepare_invoice_line(self, **a):
        # Call the super method to get the default invoice line values
        invoice_line_vals = super(SaleOrderLine, self)._prepare_invoice_line(**a)

        # Add the brand_id to the invoice line values
        invoice_line_vals.update({
            'brand_id': self.brand_id.id,
        })

        return invoice_line_vals
