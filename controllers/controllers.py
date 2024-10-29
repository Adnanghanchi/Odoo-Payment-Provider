# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentSadad(http.Controller):
#     @http.route('/payment_sadad/payment_sadad', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_sadad/payment_sadad/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_sadad.listing', {
#             'root': '/payment_sadad/payment_sadad',
#             'objects': http.request.env['payment_sadad.payment_sadad'].search([]),
#         })

#     @http.route('/payment_sadad/payment_sadad/objects/<model("payment_sadad.payment_sadad"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_sadad.object', {
#             'object': obj
#         })

