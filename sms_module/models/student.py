from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date


class Student(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('student_id_unique', 'UNIQUE(student_id)', 'Student ID must be unique!')
    ]
    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    name = fields.Char(string='Name')
    description = fields.Html(string='Description')
    date_of_birth = fields.Date(string='Date of Birth')
    contact_details = fields.Char(string='Contact Details', tracking=1)
    address = fields.Text(string='Address')
    guardian_details = fields.Text(string='Guardian Details')
    student_id = fields.Char(string="Student ID", required=True,
                             default=lambda self: self.env['ir.sequence'].next_by_code('student.id'))
    national_doc = fields.Binary(string='National Document', attachment=True)
    image = fields.Image(string='Image', attachment=True)
    email = fields.Char(string='Email')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')

    # endregion

    # region  Special
    active = fields.Boolean(string='Active', default=True)

    # endregion

    # region  Relational
    enrollment_ids = fields.One2many('sms_module.enrollment', 'student_id', string='Enrollments', tracking=1)
    grade_ids = fields.One2many('sms_module.grade', 'student_id', string='Grades')
    attendance_ids = fields.One2many('sms_module.attendance', 'student_id', string='Attendance Records')



    # endregion

    # region  Computed
    age = fields.Integer(string='Age', compute='_compute_age' , store=True)

    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                birth_date = fields.Date.from_string(record.date_of_birth)
                record.age = relativedelta(today, birth_date).years
            else:
                record.age = 0

    @api.depends('name', 'student_id')
    def _compute_display_name(self):
        for record in self:
            context = self.env.context
            if context.get('display_id', False):
                record.display_name = f"[{record.student_id}] {record.name}"
            else:
                record.display_name = record.name


    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------
    @api.constrains('student_id')
    def _check_unique_student_id(self):
        for record in self:
            if self.search_count([('student_id', '=', record.student_id)]) > 1:
                raise ValidationError('Student ID must be unique!')

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    @api.model
    def create(self, vals):
        if vals.get('student_id', 'New') == 'New':
            vals['student_id'] = self.env['ir.sequence'].next_by_code('sms_module_student_id_sequence') or 'New'
        return super(Student, self).create(vals)

    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------

    @api.model
    def get_adult_students(self):
        age_threshold = self.env.context.get('age_threshold', 18)
        adult_students = self.search([('age', '>=', age_threshold)])
        return adult_students

    @api.model
    def action_trigger_students_age(self):

        adult_students = self.with_context(age_threshold=18).get_adult_students()
        return {
            'name': 'Adult Students',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sms_module.student',
            'domain': [('id', 'in', adult_students.ids)],
        }
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, order=None):
        args = args or []
        domain = ['|', ('name', operator, name), ('student_id', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid, order=order)

    # endregion
