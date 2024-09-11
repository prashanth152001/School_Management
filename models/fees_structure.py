from odoo import models, fields, api


class FeesStructure(models.Model):
    _name = 'school.fees.structure'
    _description = 'School fees structure'
    _rec_name = 'fee_name_id'
    # name = fields.Char(string='Fees Name', required=True)
    fee_name_id = fields.Many2one(comodel_name='product.template', string='Fee Name')
    due_date = fields.Datetime(string='Due Date')
    amount = fields.Float(string='Fees Amount', required=True)
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
                tax_result = record.tax_ids.compute_all(record.amount, currency=None,
                                                        quantity=1, product=None, partner=None)
                # Calculate the tax and total amounts
                record.tax_amount = tax_result['total_included'] - tax_result['total_excluded']  # Tax amount
                record.total_amount = tax_result['total_included']  # Total amount including tax

    # Fee due remainder through email
    @api.model
    def _cron_send_email(self):
        # Logic to send email reminders
        # You can loop over fee structures and send emails based on due dates
        today = fields.Date.context_today(self)
        fee_records = self.search([('due_date', '<=', today)])

        for fee in fee_records:
            # Logic to send email to the student or guardian
            template_id = self.env.ref('school.mail_template_fee_due_remainder')
            if template_id:
                template_id.send_mail(fee.id, force_send=True)

    # Fee payment button in notebook fee structure page
    def fee_payment_button(self):
        # Create an invoice
        invoice_vals = {
            'partner_id': self.student_id.user_id.partner_id.id,  # Student's related partner
            'move_type': 'out_invoice',  # Outgoing invoice
            'parent_name': self.student_id.guardian,
            'parent_mobile': self.student_id.guardian_num,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'product_id': self.fee_name_id.id,
                'student_fee_id': self.id,
                'name': self.fee_name_id.name,
                'quantity': 1,
                'price_unit': self.amount,
                'tax_ids': [(6, 0, self.tax_ids.ids)],  # M2M relation needs this format
                'price_subtotal': self.amount,  # Fee amount for the student
                'price_total': self.total_amount,  # Total after applying taxes, if any
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fee Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
        }
