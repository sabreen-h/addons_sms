from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Attendance(models.Model):

    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.attendance"
    _description = "Attendance"
    _sql_constraints = [
        ('attendance_date_student_unique', 'UNIQUE(attendance_date, student_id)',
         'Attendance for this student on this date already exists.')
    ]
    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    attendance_date = fields.Date(string='Attendance Date')
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ], string='Status', default='present')
    # endregion

    # region  Special
    # endregion

    # region  Relational
    student_id = fields.Many2one('sms_module.student', string='Student')
    course_id = fields.Many2one('sms_module.course', string='Course')
    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------

    @api.constrains('attendance_date', 'student_id')
    def _check_unique_attendance(self):
        for record in self:
            if self.search_count(
                    [('attendance_date', '=', record.attendance_date), ('student_id', '=', record.student_id.id)]) > 1:
                raise ValidationError('Attendance for this student on this date already exists.')

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion