from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions , _
from odoo.exceptions import ValidationError
from datetime import date


class Enrollment(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.enrollment"
    _description = "Enrollment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
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
    student_id = fields.Many2one('sms_module.student', string='Student', domain=[('active', '=', True)],
                                 context={'display_id': True})
    course_id = fields.Many2one('sms_module.course', string='Course')
    course_name = fields.Char(string='Course Name', related='course_id.name', readonly=True)
    course_duration = fields.Integer(string='Course Duration', readonly=True, related='course_id.duration')
    teacher_id = fields.Many2one('res.users', string='Teacher', related='course_id.teacher_id', store=True)

    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------

    @api.onchange('course_id')
    def _onchange_course_id(self):
        for record in self:
            if record.course_id:
                record.course_duration = record.course_id.duration
            else:
                record.course_duration = 0

    @api.constrains('enrollment_date', 'student_id', 'course_id')
    def _check_unique_enrollment(self):
        for record in self:
            if self.search_count(
                    [('enrollment_date', '=', record.enrollment_date),
                     ('student_id', '=', record.student_id.id),
                     ('course_id', '=', record.course_id.id)]) > 1:
                raise ValidationError('Enrollment for this student in this course on this date already exists.')

    @api.constrains('enrollment_date')
    def _check_enrollment_date(self):
        for record in self:
            if record.enrollment_date > date.today():
                raise exceptions.ValidationError("Enrollment date cannot be in the future.")

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------

    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    def _send_enrollment_notification(self, record):
        notification_deadline = record.enrollment_date + relativedelta(days=2)
        if fields.Date.today() <= notification_deadline:
            body = _(
                "A new student, %s, has been enrolled in your course %s on %s."
                % (record.student_id.name, record.course_id.name, record.enrollment_date)
            )
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': body,
                'res_id': record.id,
                'res_model_id': self.env.ref('sms_module.model_sms_module_enrollment').id,
                'user_id': record.teacher_id.id,
                'date_deadline': notification_deadline
            })

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            self._send_enrollment_notification(record)

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
    @api.model
    def create(self, vals):
        enrollment = super(Enrollment, self).create(vals)
        enrollment._post_enrollment_message()
        return enrollment

    def write(self, vals):
        res = super(Enrollment, self).write(vals)
        if 'state' in vals:
            self._post_state_change_message()
        return res

    def _post_enrollment_message(self):
        for record in self:
            self.message_post(
                body=_("Student %s has been enrolled in the course %s on %s.") % (
                    record.student_id.name, record.course_name, record.enrollment_date),
                message_type='notification',
                subtype_xmlid='mail.mt_note'
            )

    def _post_state_change_message(self):
        for record in self:
            state_changes = {
                'confirmed': "Enrollment confirmed.",
                'completed': "Enrollment completed.",
                'cancelled': "Enrollment cancelled.",
                'draft': "Enrollment set to draft."
            }
            message = state_changes.get(record.state, "State updated.")
            self.message_post(
                body=_("Enrollment for student %s in course %s has been %s.") % (
                    record.student_id.name, record.course_name, message),
                message_type='notification',
                subtype_xmlid='mail.mt_note'
            )
    # endregion
