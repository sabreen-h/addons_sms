# -*- coding: utf-8 -*-
# from odoo import http


# class SmsModule(http.Controller):
#     @http.route('/sms_module/sms_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sms_module/sms_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sms_module.listing', {
#             'root': '/sms_module/sms_module',
#             'objects': http.request.env['sms_module.sms_module'].search([]),
#         })

#     @http.route('/sms_module/sms_module/objects/<model("sms_module.sms_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sms_module.object', {
#             'object': obj
#         })

