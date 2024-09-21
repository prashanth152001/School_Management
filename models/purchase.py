from odoo import models, fields
from datetime import datetime


class PurchaseUpgrade(models.Model):
    _inherit = 'purchase.order'

    bank_name = fields.Char(string='Bank')
    account_name = fields.Char(string='Account Name')
    account_number = fields.Char(string='Account No.')
    iban_number = fields.Char(string='IBAN No.')

    def format_custom_date(self, date_order):
        if date_order:
            # Convert the date_order (string) to a datetime object
            date_object = fields.Date.from_string(date_order)
            # Format the date in "02 June, 2024" format
            return date_object.strftime('%d %B, %Y')
        return ''

