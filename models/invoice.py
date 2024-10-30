from odoo import models, fields


class InvoiceUpgrade(models.Model):
    _inherit = 'account.move'

    parent_name = fields.Char(string='Parent Name')
    parent_mobile = fields.Char(string='Parent Mobile No.')
    # invoices for student fee payments tracking
    student_fee_id = fields.Many2one(comodel_name='school.fees.structure', string='Student Fee')
    # Banking details for inherited invoice
    bank_name = fields.Char(string='Bank Name')
    account_number = fields.Char(string='Account Number')
    ifsc_code = fields.Char(string='IFSC Code')
    branch_name = fields.Char(string='Branch Name')


class InvoiceLinesUpgrade(models.Model):
    _inherit = 'account.move.line'

    student_fee_id = fields.Many2one(comodel_name='school.fees.structure',string='Student Fee')
    brand_id = fields.Many2one(comodel_name='product.brand', string='Product Brand')