from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class Attendance(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.attendance"
    _description = "Attendance"
    _sql_constraints = [
        ('attendance_date_student_course_unique',
         'UNIQUE(attendance_date, student_id, course_id)',
         'Attendance for this student in this course on this date already exists.')
    ]

    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    @api.model
    def _default_attendance_date(self):
        return fields.Date.today()

    @api.model
    def _default_checkin_time(self):
        return fields.Datetime.now()

    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    attendance_date = fields.Date(string='Attendance Date', default=_default_attendance_date)
    checkin_time = fields.Datetime(string='Check-in Time', default=_default_checkin_time)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ], string='Status', default='present')
    absence_notes = fields.Text(string="Absence Notes")
    comments = fields.Text(string="Comments")
    class_name = fields.Char(string="Class Name")
    internal_notes = fields.Text(string="Internal Notes", invisible="True")

    # endregion

    # region  Special
    # endregion

    # region  Relational
    student_id = fields.Many2one('sms_module.student', string='Student')
    course_id = fields.Many2one('sms_module.course', string='Course')
    teacher_id = fields.Many2one(related='course_id.teacher_id', string='Teacher', store=True, readonly=True)

    # endregion

    # region  Computed

    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    #
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------

    @api.constrains('attendance_date', 'student_id', 'course_id')
    def _check_unique_attendance(self):
        for record in self:
            if self.search_count(
                    [('attendance_date', '=', record.attendance_date),
                     ('student_id', '=', record.student_id.id),
                     ('course_id', '=', record.course_id.id)]) > 1:
                raise ValidationError('Attendance for this student in this course on this date already exists.')

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    def action_generate_attendance_today(self):
        today = date.today()
        for record in self:
            if not self.search([('attendance_date', '=', today), ('student_id', '=', record.student_id.id),
                                ('course_id', '=', record.course_id.id)]):
                self.create({
                    'attendance_date': today,
                    'status': 'present',
                    'student_id': record.student_id.id,
                    'course_id': record.course_id.id
                })

    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
