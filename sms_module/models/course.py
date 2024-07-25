from odoo import models, fields, api, exceptions


class Course(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.course"
    _description = "Course"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    @api.model
    def _default_course_duration(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('sms_module.default_course_duration', default=10))

    @api.model
    def _max_students_per_course(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('sms_module.max_students_per_course', default=30))

    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    name = fields.Char(string='Name')
    description = fields.Html(string='Description', tracking=1)
    syllabus = fields.Text(string='Syllabus')
    duration = fields.Integer(string='Duration (weeks)')
    prerequisites = fields.Text(string='Prerequisites')
    is_featured = fields.Boolean(string='Featured Course')
    course_level = fields.Integer(string='Course Level')

    # endregion

    # region  Special
    # endregion

    # region  Relational
    enrollment_ids = fields.One2many('sms_module.enrollment', 'course_id', string='Enrollments')
    teacher_id = fields.Many2one('res.users', string='Teacher')

    # endregion

    # region  Computed
    enrollment_count = fields.Integer(string='Enrollment Count', compute='_compute_enrollment_count')
    completion_percentage = fields.Float(string='Completion Percentage', compute='_compute_completion_percentage',
                                         store=True)

    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    @api.depends('enrollment_ids')
    def _compute_enrollment_count(self):
        for course in self:
            course.enrollment_count = len(course.enrollment_ids)

    @api.depends('enrollment_ids')
    def _compute_completion_percentage(self):
        for course in self:
            total_enrollments = len(course.enrollment_ids)
            max_enrollment = self._max_students_per_course()
            course.completion_percentage = total_enrollments / max_enrollment * 100

    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------
    @api.constrains('enrollment_ids')
    def _check_max_students(self):
        for course in self:
            max_students = self._max_students_per_course()
            if len(course.enrollment_ids) > max_students:
                raise exceptions.ValidationError(
                    f"Cannot enroll more than {max_students} students in the course '{course.name}'.")

    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    @api.model
    def create(self, vals):
        if 'duration' not in vals:
            vals['duration'] = self._default_course_duration()
        return super(Course, self).create(vals)

    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    def action_view_enrollments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Enrollments',
            'view_mode': 'tree,form',
            'res_model': 'sms_module.enrollment',
            'domain': [('course_id', '=', self.id)],
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
