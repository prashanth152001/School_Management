from odoo import models, fields, api
from datetime import datetime


class SchoolParents(models.Model):
    _name = 'school.parents'
    _description = 'School Parent Records'

    name = fields.Char(string='Parent Name', required = True)
    mobile_num = fields.Char(string='Mobile Number')
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(string='Age', compute='_compute_parent_age', store=True)
    child_id = fields.Many2one(comodel_name='school.student', string='Child')
    child_class = fields.Char(string='Child Class')


    # age computation from date of birth
    @api.depends('dob')
    def _compute_parent_age(self):
        today = datetime.today().date()
        if self.dob:
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            self.age = age
        else:
            self.age = 0

    # onchange method to get child class when child_id is selected
    @api.onchange('child_id')
    def _onchange_child_id(self):
        if self.child_id:
            self.child_class = self.child_id.standard
        else:
            self.child_class = 0