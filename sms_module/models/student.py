from odoo import models, fields, api
class Student(models.Model):

    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _name = "sms_module.student"
    _description = " Student"
    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------
    name = fields.Char(string='Name')
    description = fields.Html(string='Description')
    date_of_birth = fields.Date(string='Date of Birth')
    contact_details = fields.Char(string='Contact Details')
    address = fields.Text(string='Address')
    guardian_details = fields.Text(string='Guardian Details')
    student_id = fields.Char(string='Student ID')
    national_doc = fields.Binary(string='National Document' , attachment=True)
    image = fields.Image(string='Image' , attachment=True)

    # endregion

    # region  Special
    # endregion

    # region  Relational
    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------
    _sql_constraints = [
        ('student_id_unique', 'UNIQUE(student_id)', 'Student ID must be unique!')
    ]
    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion