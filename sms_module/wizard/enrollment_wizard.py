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
    def enroll_students(self):
        Enrollment = self.env['sms_module.enrollment']
        for wizard in self:
            for student in wizard.student_ids:
                if not Enrollment.search([('student_id', '=', student.id), ('course_id', '=', wizard.course_id.id)]):
                    Enrollment.create({
                        'student_id': student.id,
                        'course_id': wizard.course_id.id,
                        'enrollment_date': fields.Date.today(),
                    })
                else:
                    raise ValidationError(
                        f'The student {student.name} is already enrolled in the course {wizard.course_id.name}.')
        return {'type': 'ir.actions.act_window_close'}

    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
