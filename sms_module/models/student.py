from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    description = fields.Html(string='Description', tracking=1)
    date_of_birth = fields.Date(string='Date of Birth')
    contact_details = fields.Char(string='Contact Details', tracking=1)
    address = fields.Text(string='Address')
    guardian_details = fields.Text(string='Guardian Details')
    student_id = fields.Char(string="Student ID", required=True, default=lambda self: self.env['ir.sequence'].next_by_code('STD'))
    national_doc = fields.Binary(string='National Document', attachment=True)
    image = fields.Image(string='Image', attachment=True)

    # endregion

    # region  Special
    active = fields.Boolean(string='Active', default=True)

    # endregion

    # region  Relational
    enrollment_ids = fields.One2many('sms_module.enrollment', 'student_id', string='Enrollments', tracking=1)

    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------
    @api.constrains('student_id')
    def _check_unique_student_id(self):
        for record in self:
            if self.search_count([('student_id', '=', record.student_id)]) > 1:
                raise ValidationError('Student ID must be unique!')

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, order=None):
        args = args or []
        domain = ['|', ('name', operator, name), ('student_id', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid, order=order)

    # endregion
