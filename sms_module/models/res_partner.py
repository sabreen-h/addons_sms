from odoo import models, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    student_id = fields.Integer(string='Student ID')
