import os
from flask import Flask, redirect, request, jsonify, Blueprint
from flask_cors import CORS
import stripe


stripe_api = Blueprint('stripeApi', __name__)
stripe.api_key = os.getenv('BACKSTRIPEKEY')
CORS(stripe_api)  # Allow CORS requests to this API

@stripe_api.route('/payment-checkout', methods=['POST'])
def payment_checkout():
    try:
        data = request.json
        intent = stripe.PaymentIntent.create(
            amount = data['amount'],
            currency = data['currency'],
            automatic_payment_methods={
                'enabled': True
            }
        )
        return jsonify({ 'clientSecret': intent['client_secret']})
        
    except Exception as e:
        return jsonify({ 'success': False, 'error': str(e)})
