from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import logging
from odoo.addons.payment_sadad.const import PAYMENT_STATUS_MAPPING
from odoo.http import request
from .sadad_checksum import get_checksum_hash
_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    sadad_txn_id = fields.Char("Sadad Transaction ID")


    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)


        _logger.info(processing_values)
        if self.provider_code != 'sadad':
            return res

        
        # Get the current website domain
        website = self.env['website'].get_current_website()
        current_domain = website.domain if website else self.provider_id.sadad_domain

        # Prepare the rendering values for Sadad
        sale_order = self.env['sale.order'].search([('name', '=', self.reference)], limit=1)
        product_details = []
        for line in sale_order.order_line:
            if line.product_id.type != 'service':  # Exclude service products
                product_details.append({
                    'order_id': self.reference,
                    'amount': format(line.price_unit, '.2f'),  # Ensure amount is in string format with 2 decimal places
                    'quantity': int(line.product_uom_qty),  # Ensure quantity is an integer
                })

        # Prepare the rendering values for Sadad
        rendering_values = {
            'merchant_id': self.provider_id.sadad_merchant_id, 
            'ORDER_ID': self.reference, 
            'WEBSITE': "odoo.secretdemo.com",
            'TXN_AMOUNT': str(self.amount),
            'CUST_ID': self.partner_id.email,
            'EMAIL': self.partner_id.email,
            'MOBILE_NO': self.partner_id.phone,
            'SADAD_WEBCHECKOUT_PAGE_LANGUAGE': self.provider_id.sadad_language,
            'CALLBACK_URL':  str(current_domain) + '/payment/sadad/return',
            'txnDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
            'productdetail': product_details
        }
        merchant_id = self.provider_id.sadad_merchant_id
        secret_key = self.provider_id.sadad_secret_key
        check_sum_hash_class = get_checksum_hash()
        # Calculate checksum
        rendering_values['checksumhash'] = check_sum_hash_class.get_hash_string(rendering_values,secret_key,merchant_id)
        return rendering_values

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'sadad' or len(tx) == 1:
            return tx

        reference = notification_data.get('ORDERID')
        if not reference:
            raise ValidationError(
                "Sadad: " + _("Received data with missing reference %(ref)s.", ref=reference)
            )

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'sadad')])
        if not tx:
            raise ValidationError(
                "Sadad: " + _("No transaction found matching reference %s.", reference)
            )

        return tx


    def _handle_notification_data(self, provider_code, notification_data):
        if provider_code != 'sadad':
            return super()._handle_notification_data(provider_code, notification_data)

        self._process_notification_data(notification_data)

    def _process_notification_data(self, notification_data):
        #super()._process_notification_data(notification_data)
        if self.provider_code != 'sadad':
            return super()._process_notification_data(notification_data)

        if not notification_data:
            self._set_canceled(_("The customer left the payment page."))
            return 

        self.provider_reference = notification_data.get('transaction_number')
        self.sadad_txn_id = notification_data.get('transaction_number')
        
        # Set Sadad as the payment method if not already set
        if not self.payment_method_id:
            self.payment_method_id = self.env['payment.method'].search([('code', '=', 'sadad')], limit=1)

        if not self.payment_method_id:
            raise ValidationError(_("Please define a payment method line on your payment.23"))


        # Update the payment state.
        status_code = notification_data.get('RESPCODE')
        if not status_code:
            raise ValidationError("Sadad: " + _("Received data with missing payment state."))
        
        if not status_code:
            raise ValidationError("Missing response code")

        if status_code == '1':
            self._set_done()
        elif status_code in ['400', '402']:
            self._set_pending()
        elif status_code == '810':
            self._set_error("Transaction failed with Sadad")

    def _finalize_post_processing(self):
        if not self.payment_method_id:
            self.payment_method_id = self.env['payment.method'].search([('code', '=', 'sadad')], limit=1)

        if not self.payment_method_id:
            #raise ValidationError(_()) 
            _logger.info("Please define a payment method line on your payment.")

        super(PaymentTransaction, self)._finalize_post_processing()
        