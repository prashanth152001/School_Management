from odoo import models, fields


class SchoolAdmission(models.Model):
    _name = 'school.admission'
    _description = 'School Admission'

    name = fields.Char(string='Student Name', required=True)
    dob = fields.Date(string='Date of Birth')
    parent = fields.Char(string='Guardian Name')
    parent_num = fields.Char(string='Guardian Mobile Number')
    standard = fields.Integer()
    admission_status = fields.Selection([('draft', 'Draft'), ('admitted', 'Admitted')
                                      ], default='draft')


    def student_creation(self):
        self.admission_status = 'admitted'
        student = self.env['school.student'].create({
            'name': self.name,
            'dob': self.dob,
            'guardian': self.parent,
            'guardian_num': self.parent_num,
            'standard': self.standard,
        })