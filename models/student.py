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
    student_image = fields.Image(string='Student Image')

    # total fee amounts and tax amount calculation
    final_total_amount = fields.Float(string='Total:', compute='_compute_total_amount', store=True, readonly=True)
    untaxed_amount = fields.Float(string='Untaxed Amount:',compute='_compute_total_amount', store=True, readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount:', compute='_compute_total_amount', store=True, readonly=True)

    #invoice count
    invoice_count = fields.Float(string='Invoice Count', compute='_compute_invoice_count')

    # computing student suggestions count
    def _compute_complaints_count(self):
        self.complaints_count = self.env['student.complaint'].search_count(
            domain=[('name', '=', self.name)]
        )

    # student complaint wizard
    def student_complaint_creation_button(self):
        return {
            'name': _('Complaint'),
            'type': 'ir.actions.act_window',
            'res_model': 'student.complaint.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': "{'default_name_id': active_id}"
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
        self.user_id = student_user.id

    # student email button action
    def action_student_email_button(self):
        template = self.env.ref('school.mail_template_student_creation')
        template.send_mail(self.id)

    # automatically fetching teacher mobile no. when a teacher is selected
    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id:
            self.teacher_mob_num = self.teacher_id.mob_num

    # computing total amounts
    @api.depends('fees_structure_ids')
    def _compute_total_amount(self):
        """Compute the total untaxed amount, taxed amount, and total amount from fees structures."""
        for rec in self:
            # Initialize the amounts to 0
            rec.untaxed_amount = 0.0
            rec.taxed_amount = 0.0
            rec.final_total_amount = 0.0

            # Sum the amounts from the fees_structure_ids recordset
            for fee in rec.fees_structure_ids:
                rec.untaxed_amount += fee.amount
                rec.taxed_amount += fee.tax_amount
                rec.final_total_amount += fee.total_amount

    # Full fee payment button
    def full_payment_button(self):
        # Collect invoice lines from fee structure
        invoice_lines = []
        for rec in self.fees_structure_ids:
            invoice_lines.append((0, 0, {
                'product_id': rec.fee_name_id.id,
                'student_fee_id': rec.id,
                'name': rec.fee_name_id.name,
                'quantity': 1,
                'price_unit': rec.amount,
                'tax_ids': [(6, 0, rec.tax_ids.ids)],  # M2M relation needs this format
                'price_subtotal': rec.amount,  # The amount before tax
                'price_total': rec.total_amount,  # Total after applying taxes, if any
            }))
        # Invoice values
        invoice_vals = {
            'partner_id': self.user_id.partner_id.id,
            'parent_name': self.guardian,
            'parent_mobile': self.guardian_num,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,  # Use the constructed list of lines
        }
        # Create invoice
        invoice = self.env['account.move'].create(invoice_vals)
        # Return action to open the created invoice
        return {
            'type': 'ir.actions.act_window',
            'name': 'Full Fee Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
        }

    # computing invoice count
    def _compute_invoice_count(self):
        self.invoice_count = self.env['account.move'].search_count(
            domain=[('partner_id', '=', self.user_id.partner_id.id), ('move_type', '=', 'out_invoice')],
        )

    # viewing fee invoices
    def action_view_fee_invoice(self):
        return {
            'name': _('Invoices'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('partner_id', '=', self.user_id.partner_id.id), ('move_type', '=', 'out_invoice')],
        }

