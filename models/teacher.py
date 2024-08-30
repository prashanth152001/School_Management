from email.policy import default

from odoo import models, fields

class TeacherDetails(models.Model):
    _name = 'school.teacher'
    _inherit = ['mail.thread']
    _description = 'school teacher'

    name = fields.Char(string='Teacher Name', required=True, tracking=True)
    address = fields.Char(string='Teacher Address')
    mob_num = fields.Char(string='Mobile number', tracking=True)
    dob = fields.Date(string='Date of Birth')
    class_teacher = fields.Boolean()
    seniority = fields.Selection([('junior','Junior'),
                                  ('senior','Senior')], default='junior')

    def action_select(self):
        self.seniority = 'senior'