from odoo import models, fields


class StudentComplaint(models.Model):
    _name = 'student.complaint'
    _description = 'Student Complaint'

    name = fields.Char(string='Student Name', required=True)
    student_class = fields.Char(string='Class')
    suggestions = fields.Text(string='Suggestions')
