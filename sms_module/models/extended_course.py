from odoo import models, fields


class ExtendedCourse(models.Model):
    _inherit = 'sms_module.course'
    _name = 'sms_module.extended_course'
    _description = 'Extended Course'

    course_prerequisite = fields.Text(string='Course Prerequisite')
