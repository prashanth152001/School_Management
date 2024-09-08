from odoo import models, fields


class TeacherDetails(models.Model):
    _name = 'school.teacher'
    _inherit = ['mail.thread']
    _description = 'school teacher'

    name = fields.Char(string='Teacher Name', required=True, tracking=True)
    email = fields.Char(string='Email')
    address = fields.Char(string='Teacher Address')
    mob_num = fields.Char(string='Mobile number', tracking=True)
    dob = fields.Date(string='Date of Birth')
    class_teacher = fields.Boolean()
    joining_status = fields.Selection([('draft','Draft'),
                                  ('joined','Joined')], default='draft')
    user_id = fields.Many2one('res.users', string='User')

    # teacher user creation and changing status bar action
    def action_teacher_user_creation(self):
        self.joining_status = 'joined'
        teacher_user = self.env['res.users'].create({
            'name': self.name,
            'login': self.email,
            'groups_id': [(6, 0, [self.env.ref('school.group_school_teacher').id])],
            'password': 'teacher',
        })
        self.user_id = teacher_user.id



