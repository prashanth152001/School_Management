from odoo import models, fields, api, _


class StudentDetails(models.Model):
    _name = 'school.student'
    _inherit = ['mail.thread']
    _description = 'school student'

    name = fields.Char(string='Student Name', required=True, tracking=True)
    email_address = fields.Char(string='Email')
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
    complaints_count = fields.Float(string='Complaints Count', compute='_compute_complaints_count')
    user_id = fields.Many2one(comodel_name='res.users', string='User')


    # computing student suggestions count
    def _compute_complaints_count(self):
        self.complaints_count = self.env['student.complaint'].search_count(
            domain=[('name', '=', self.name)],
        )

    # student complaint wizard
    def student_complaint_creation_button(self):
        return {
            'name': _('Complaint'),
            'type': 'ir.actions.act_window',
            'res_model': 'student.complaint.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context':"{'default_name_id': active_id}"
        }

    # suggestions smart button
    def action_open_student_suggestions(self):
        return {
            'name': _('Suggestions'),
            'type': 'ir.actions.act_window',
            'res_model': 'student.complaint',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('name', '=', self.name)],
        }

    # action for status bar selection button and user creation for student group
    def action_student_admit(self):
        self.select_status = 'admitted'
        student_user = self.env['res.users'].create({
            'name': self.name,
            'login': self.email_address,
            'groups_id': [(6, 0, [self.env.ref('school.group_school_student').id])],
            'password': 'student',
        })

    # automatically fetching teacher mobile no. when a teacher is selected
    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id:
            self.teacher_mob_num = self.teacher_id.mob_num



