import logging
import pprint
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from Cryptodome.Cipher import AES
import base64
import hashlib
import json

_logger = logging.getLogger(__name__)

class SadadController(http.Controller):
    _return_url = "/payment/sadad/return"


    @http.route(['/payment/sadad/return'], methods=['POST'], type='http', auth='public', website=True, csrf=False, save_session=False)
    def sadad_return(self, **data):
         
        _logger.info("Received data from Sadad: %s", pprint.pformat(data))
    
        order_id = data.get('ORDERID')
        if not order_id:
            _logger.info('Transaction not found for ORDER_ID: %s', order_id)
            return "ORDERID not found"  # Handle accordingly
        else:
            _logger.info('Transaction found for ORDER_ID: %s', order_id)
                
        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', order_id)])
        if not transaction:
            _logger.error('Transaction not found for ORDER_ID: %s', order_id)
            return "Transaction not found"  # Handle accordingly
        
        _logger.info("Transaction: %s", transaction.reference)
        
        try:
            status_code = data.get('RESPCODE')
            if status_code == '1':
                _logger.info("Checksum verified successfully for transaction: %s", transaction.reference)
                transaction._handle_notification_data('sadad',data)
                _logger.info("Transaction successfully processed: %s", transaction.reference)
                return request.redirect('/payment/status')
            else:
                transaction._handle_notification_data('sadad',data)
                _logger.info('Transaction failed with RESPCODE: %s for transaction: %s', status_code, transaction.reference)
                
                return request.redirect('/payment/status')
        except ValidationError as e:
            transaction._handle_notification_data('sadad',data)
            _logger.info('Transaction processing failed for transaction: %s. Error: %s', transaction.reference, str(e))
            return request.redirect('/payment/status')
          
    def _remove_products_from_cart(self, transaction):
        sale_order = request.env['sale.order'].sudo().search([('name', '=', transaction.reference)], limit=1)
        if sale_order:
            sale_order.action_cancel()
            for line in sale_order.order_line:
                line.unlink()
            sale_order.unlink()
            _logger.info('Products removed from cart for sale order: %s', sale_order.name)
    