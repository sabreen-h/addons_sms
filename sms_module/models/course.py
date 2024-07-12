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
    description = fields.Html(string='Description', tracking=1)
    syllabus = fields.Text(string='Syllabus')
    duration = fields.Integer(string='Duration (weeks)')
    prerequisites = fields.Text(string='Prerequisites')
    is_featured = fields.Boolean(string='Featured Course')

    # endregion

    # region  Special
    # endregion

    # region  Relational
    enrollment_ids = fields.One2many('sms_module.enrollment', 'course_id', string='Enrollments')

    # endregion

    # region  Computed
    enrollment_count = fields.Integer(string='Enrollment Count', compute='_compute_enrollment_count')

    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    @api.depends('enrollment_ids')
    def _compute_enrollment_count(self):
        for course in self:
            course.enrollment_count = len(course.enrollment_ids)
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Enrollments',
            'view_mode': 'tree,form',
            'res_model': 'sms_module.enrollment',
            'domain': [('course_id', '=', self.id)],
            'context': "{'default_course_id': %d}" % self.id,
        }

    def action_open_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://www.odoo.com',
            'target': 'new',
        }
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
