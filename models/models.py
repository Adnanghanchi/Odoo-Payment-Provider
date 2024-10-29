# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class payment_sadad(models.Model):
#     _name = 'payment_sadad.payment_sadad'
#     _description = 'payment_sadad.payment_sadad'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

