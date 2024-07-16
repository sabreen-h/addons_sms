from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EnrollmentWizard(models.TransientModel):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.enrollment_wizard"
    _description = "Enrollment Wizard"

    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------

    # endregion

    # region  Special
    # endregion

    # region  Relational
    student_ids = fields.Many2many('sms_module.student', string='Students')
    course_id = fields.Many2one('sms_module.course', string='Course')
    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------

    def action_enroll_students(self):
        enrollments = []
        for student in self.student_ids:
            enrollments.append({
                'enrollment_date': fields.Date.today(),
                'student_id': student.id,
                'course_id': self.course_id.id,
            })
        self.env['sms_module.enrollment'].create(enrollments)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Students enrolled successfully.',
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
                'sticky': False,
            }
        }

    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
