from odoo import models, fields, api
from datetime import timedelta

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
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    attendance_date = fields.Date(string='Attendance Date', default=lambda self: fields.Date.today())
    checkin_time = fields.Datetime(string='Check-in Time', default=lambda self: fields.Datetime.now())
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
    # endregion

    # region  Computed
    yesterday_date = fields.Date(string="Yesterday", compute="_compute_yesterday_date", store=True)
    last_4_weeks_start_date = fields.Date(string="Last 4 Weeks Start", compute="_compute_last_4_weeks_start_date",
                                          store=True)

    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    @api.depends('attendance_date')
    def _compute_yesterday_date(self):
        for record in self:
            if record.attendance_date:
                record.yesterday_date = record.attendance_date - timedelta(days=1)

    @api.depends('attendance_date')
    def _compute_last_4_weeks_start_date(self):
        for record in self:
            if record.attendance_date:
                record.last_4_weeks_start_date = record.attendance_date - timedelta(days=7 * 4)

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
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
