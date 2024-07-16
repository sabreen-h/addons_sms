from odoo import models, fields


class EmergencyContact(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = 'sms_module.emergency_contact'
    _description = 'Emergency Contact'
    _inherits = {'res.partner': 'partner_id'}

    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    contact_type = fields.Selection([
        ('emergency', 'Emergency'),
        ('alternate', 'Alternate')
    ], string='Contact Type', required=True)
    # region  Basic
    # endregion

    # region  Special
    # endregion

    # region  Relational
    partner_id = fields.Many2one('res.partner', auto_join=True, index=True, required=True, ondelete="cascade")

    student_id = fields.Many2one('sms_module.student', string='Student ID', required=True)

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
