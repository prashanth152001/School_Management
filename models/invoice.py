from odoo import models, fields


class InvoiceUpgrade(models.Model):
    _inherit = 'account.move'

    parent_name = fields.Char(string='Parent Name')
    parent_mobile = fields.Char(string='Parent Mobile No.')


class InvoiceLinesUpgrade(models.Model):
    _inherit = 'account.move.line'

    student_fee_id = fields.Many2one(comodel_name='school.fees.structure',string='Student Fee')
