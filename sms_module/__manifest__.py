# -*- coding: utf-8 -*-
{
    'name': "sms_module",

    'summary': "Student Management System",

    'description': """
     This system will manage student information, courses, enrollments, grades, attendance, and more. The goal is to create a modular, scalable, and user-friendly application that covers various aspects of school administration.

    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'data/student_id_sequence.xml',
        'data/ir_cron_data.xml',
        'views/student_views.xml',
        'views/course_views.xml',
        'views/enrollment_views.xml',
        'views/grade_views.xml',
        'views/attendance_views.xml',
        'views/res_partner_view.xml',
        'views/extended_course_views.xml',
        'views/emergency_contact_views.xml',
        'views/res_config_settings_view.xml',

        'wizard/make_enrollment_wizard_views.xml',

        'views/report/report_student.xml',


        'views/menus.xml',

        'data/demo_data.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'sms_module/static/description/icon.png',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'data/demo_data.xml',
    ],


}
