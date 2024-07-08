from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Enrollment(models.Model):

    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.enrollment"
    _description = "Enrollment"
    _sql_constraints = [
        ('student_course_unique', 'UNIQUE(student_id, course_id)', 'The student is already enrolled in this course.')
    ]
    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    enrollment_date = fields.Date(string='Enrollment Date')
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

    @api.constrains('student_id', 'course_id')
    def _check_unique_enrollment(self):
        for record in self:
            if self.search_count(
                    [('student_id', '=', record.student_id.id), ('course_id', '=', record.course_id.id)]) > 1:
                raise ValidationError('The student is already enrolled in this course.')


    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion