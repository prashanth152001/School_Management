from odoo import models, fields, api, _


class StudentDetails(models.Model):
    _name = 'school.student'
    _inherit = ['mail.thread']
    _description = 'school student'

    name = fields.Char(string='Student Name', required=True, tracking=True)
    address = fields.Char(string='Student Address')
    guardian = fields.Char(string='Guardian Name')
    guardian_num = fields.Char(string='Guardian Mobile Number')
    dob = fields.Date(string='Date of Birth')
    doj = fields.Date(string='Date of joining')
    standard = fields.Integer()
    section = fields.Char()
    teacher_id = fields.Many2one(comodel_name='school.teacher', string='Class Teacher')
    subject_teachers_ids = fields.Many2many(comodel_name='school.teacher', string='Subject Teachers')
    select_status = fields.Selection([('draft', 'Draft'), ('admitted', 'Admitted')
                                      ], default='draft', tracking=True)
    teacher_mob_num = fields.Char(string='Teacher No.')
    fees_structure_ids = fields.One2many(comodel_name='school.fees.structure', inverse_name='student_id',
                                         string='Fees Structure')

    # student complaint wizard
    def student_complaint_creation_button(self):
        return {
            'name': _('Complaint'),
            'type': 'ir.actions.act_window',
            'res_model': 'student.complaint.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_select(self):
        self.select_status = 'admitted'

    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id:
            self.teacher_mob_num = self.teacher_id.mob_num



