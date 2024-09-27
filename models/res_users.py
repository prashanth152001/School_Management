from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    payment_terms = fields.Char(string="Payment Terms")