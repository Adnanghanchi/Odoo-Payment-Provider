from odoo import fields, models
import hashlib
from Cryptodome.Cipher import AES
import base64
import random
import string
import json
import logging
_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('sadad', "Sadad")], ondelete={'sadad': 'set default'})
    sadad_merchant_id = fields.Char(string="Sadad Merchant ID", required_if_provider='sadad')
    sadad_secret_key = fields.Char(string="Sadad Secret Key", required_if_provider='sadad', groups='base.group_system')
    sadad_domain = fields.Char(string="Domain", required_if_provider='sadad')
    sadad_api_url = fields.Char(string="Sadad CheckSum API URL", default='https://sadadqa.com/webpurchase', required_if_provider='sadad')
    sadad_web_checkout = fields.Selection([
        ('2.1', 'Web Checkout 2.1'),
        ('2.2', 'Web Checkout 2.2'),
    ], string='Web Checkout API Ver')
    sadad_language = fields.Selection([
        ('ARB', 'Arabic'),
        ('ENG', 'English'),
    ], string="Language")
    sadad_qa_webcheckout_hide_loader = fields.Selection([
        ('YES', 'Yes'),
        ('NO', 'No')
    ], string='Hide Loader', default='NO')
    sadad_qa_showdialog = fields.Selection([
        ('1', 'Modal Popup'),
        ('2', 'iFrame')
    ], string='Show Dialog', default='1')

    def _sadad_get_api_url(self):
        return self.sadad_api_url


    #=== BUSINESS METHODS ===#

    def _get_supported_currencies(self):
        """ Override to return only QAR currency. """
        self.ensure_one()
        if self.code == 'sadad':
            return self.env['res.currency'].search([('name', '=', 'QAR')])
        return super()._get_supported_currencies()

