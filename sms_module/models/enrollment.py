from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.enrollment"
    _description = "Enrollment"
    _sql_constraints = [
        ('student_course_enrollment_date_unique',
         'UNIQUE(student_id, course_id, enrollment_date)',
         'The student is already enrolled in this course on this date.')
    ]

    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    enrollment_date = fields.Date(string='Enrollment Date', default=lambda self: fields.Date.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', tracking=True)

    # endregion

    # region  Special
    # endregion

    # region  Relational
    student_id = fields.Many2one('sms_module.student', string='Student', domain=[('active', '=', True)])
    course_id = fields.Many2one('sms_module.course', string='Course')

    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------
    @api.constrains('enrollment_date', 'student_id', 'course_id')
    def _check_unique_enrollment(self):
        for record in self:
            if self.search_count(
                    [('enrollment_date', '=', record.enrollment_date),
                     ('student_id', '=', record.student_id.id),
                     ('course_id', '=', record.course_id.id)]) > 1:
                raise ValidationError('Enrollment for this student in this course on this date already exists.')

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_complete(self):
        for record in self:
            record.state = 'completed'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_draft(self):
        for record in self:
            record.state = 'draft'
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
