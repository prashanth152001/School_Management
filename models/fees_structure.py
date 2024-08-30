from odoo import models, fields

class FeesStructure(models.Model):
    _name = 'school.fees.structure'
    _inherit = ['mail.thread']
    _description = 'School fees structure'

    name = fields.Char(string='Fees Name', required=True, tracking=True)
    amount = fields.Float(string='Fees Amount', required=True, tracking=True)
    due_date = fields.Date(string='Due Date')
    student_id = fields.Many2one(comodel_name='school.student', string='Student')