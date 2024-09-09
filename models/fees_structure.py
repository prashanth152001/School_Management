from odoo import models, fields, api

class FeesStructure(models.Model):
    _name = 'school.fees.structure'
    _inherit = ['mail.thread']
    _description = 'School fees structure'

    name = fields.Char(string='Fees Name', required=True, tracking=True)
    due_date = fields.Date(string='Due Date')
    amount = fields.Float(string='Fees Amount', required=True, tracking=True)
    tax_ids = fields.Many2many(comodel_name='account.tax', string='Taxes')
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_tax_amount', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_tax_amount', store=True)
    student_id = fields.Many2one(comodel_name='school.student', string='Student')

    # Tax Amount computation
    @api.depends('amount', 'tax_ids')
    def _compute_tax_amount(self):
        for record in self:
            # Initialize the tax amount and total amount
            record.tax_amount = 0.0
            record.total_amount = record.amount

            # Check if there are taxes to apply
            if record.tax_ids:
                # Compute taxes using the entire tax_ids recordset
                tax_result = record.tax_ids.compute_all(record.amount, currency=None, quantity=1, product=None,
                                                        partner=None)

                # Calculate the tax and total amounts
                record.tax_amount = tax_result['total_included'] - tax_result['total_excluded']  # Tax amount
                record.total_amount = tax_result['total_included']  # Total amount including tax
