Payment Provider for Odoo
===============================

This module integrates the payment gateway with Odoo, enabling secure and seamless online payments.

Installation
------------

1. Clone the module repository into your Odoo addons directory.
2. Update the module list in Odoo.
3. Install the `Custom Payment Provider` module.

Configuration
-------------

Follow these steps to configure the payment provider in Odoo:

1. **Merchant ID and Secret Key:**
   - Obtain your Merchant ID and Secret Key from the custom panel.

2. **Web Checkout Overview:**
   - **Web Checkout 2.1:** Customers fill in details and place orders on your website's checkout page.

3. **Configuration Steps in Odoo:**
   - Navigate to `Payment Providers` in Odoo.
   - Enable the custom payment method and toggle test mode if needed.
   - Fill in the required fields:
     - Merchant ID
     - Client Secret Key
     - Domain (without http or https, e.g., abc1234.com)
     - Web Checkout API version
     - Language (Arabic or English)

.. image:: https://res.cloudinary.com/dqioxqal2/image/upload/v1730188505/sadad1_bnu6nr.png
   :alt: custom Payment Configuration in Odoo
   :width: 80%

4. **custom Payment Panel Configuration:**
   - Set the domain in the Custom panel.
   - Generate test or live secret keys by clicking the "Generate" button.
   - Ensure both the e-commerce website domain and the custom panel domain are the same.

.. .. image:: https://res.cloudinary.com/dqioxqal2/image/upload/v1730188505/sadad2_fnvuzs.png
..    :alt: Sadad Payment Panel Configuration
..    :width: 80%

5. **Callback URL Configuration:**
   - Set the callback URL to redirect to the e-commerce site after payment completion.
   - Example format: `https://abc1234.com/payment/custom/return`
   - Set an alert email to receive notifications from custom.

.. .. image:: https://res.cloudinary.com/dqioxqal2/image/upload/v1730188504/sadad3_tjmhzh.png
..    :alt: Callback URL Configuration
..    :width: 80%

Usage
-----

1. During checkout, users can select custom as a payment option on your website.
2. After clicking "Pay Now," users will be redirected to the custom payment screen to complete the transaction.

.. image:: https://res.cloudinary.com/dqioxqal2/image/upload/v1730188504/sadad4_qhzhsw.png
   :alt: custom Payment Option in Website
   :width: 80%

Features
--------

- Integrate custom Payment Gateway with Odoo eCommerce.
- Supports Web Checkout API versions 2.1 and 2.2.
- Allows users to set language preference (Arabic or English).
- Easy to configure and use.

.. image:: https://res.cloudinary.com/dqioxqal2/image/upload/v1730188504/sadad5_h1ln89.png
   :alt: Redirect in Payment Screen
   :width: 80%


.. image:: https://res.cloudinary.com/dqioxqal2/image/upload/v1730188505/sadad6_n2kavg.png
   :alt: Success Transaction
   :width: 80%

Support
-------

For any issues or support, please contact us.