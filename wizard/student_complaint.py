from odoo import models, fields, api


class StudentComplaintWizard(models.TransientModel):
    _name = 'student.complaint.wizard'
    _description = 'Student Complaint Wizard'

    name_id = fields.Many2one(comodel_name='school.student', string='Student Name', required=True)
    student_class = fields.Char(string='Class')
    suggestions = fields.Text(string='Suggestions')

    @api.onchange('name_id')
    def _onchange_name_id(self):
        if self.name_id:
            self.student_class = self.name_id.standard

    # storing records in Model rather than Transient Model
    def student_complaint_button(self):
        complaint = self.env['student.complaint'].create({
            'name': self.name_id.name,
            'student_class': self.student_class,
            'suggestions': self.suggestions,
        })
