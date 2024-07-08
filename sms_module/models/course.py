from odoo import models, fields, api
class Course(models.Model):

    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.course"
    _description = "Course"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    name = fields.Char(string='Name')
    description = fields.Html(string='Description' , tracking=1)
    syllabus = fields.Text(string='Syllabus')
    duration = fields.Integer(string='Duration (weeks)')
    prerequisites = fields.Text(string='Prerequisites')
    # endregion

    # region  Special
    # endregion

    # region  Relational
    enrollment_ids = fields.One2many('sms_module.enrollment', 'course_id', string='Enrollments')

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
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion