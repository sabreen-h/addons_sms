from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _name = 'res.config.settings'
    _inherit = 'res.config.settings'

    default_duration = fields.Integer(
        string='Default Course Duration',
        config_parameter='sms_module.default_course_duration',
        default=10,
        help="Default duration for courses in the SMS module.",
        default_model='sms_module.course',
    )
    max_students_per_course = fields.Integer(
        string='Maximum Number of Students per Course',
        config_parameter='sms_module.max_students_per_course',
        default=30,
        help="Maximum number of students allowed per course.",
        default_model='res.config.settings',
    )
