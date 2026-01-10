from flask import Flask, request, jsonify
import stripe
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Use service role key for admin access
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        app.logger.error(f"Invalid payload: {e}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        app.logger.error(f"Invalid signature: {e}")
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Log the event
    log_webhook_event(event)
    
    # Handle the event
    event_type = event['type']
    
    try:
        if event_type == 'checkout.session.completed':
            handle_checkout_completed(event['data']['object'])
        
        elif event_type == 'customer.subscription.created':
            handle_subscription_created(event['data']['object'])
        
        elif event_type == 'customer.subscription.updated':
            handle_subscription_updated(event['data']['object'])
        
        elif event_type == 'customer.subscription.deleted':
            handle_subscription_deleted(event['data']['object'])
        
        elif event_type == 'invoice.payment_succeeded':
            handle_invoice_payment_succeeded(event['data']['object'])
        
        elif event_type == 'invoice.payment_failed':
            handle_invoice_payment_failed(event['data']['object'])
        
        else:
            app.logger.info(f"Unhandled event type: {event_type}")
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def log_webhook_event(event):
    """Log webhook event to database"""
    try:
        supabase.table('webhook_events').insert({
            'event_id': event['id'],
            'event_type': event['type'],
            'payload': json.dumps(event),
            'processed': False
        }).execute()
    except Exception as e:
        app.logger.error(f"Error logging webhook event: {str(e)}")

def handle_checkout_completed(session):
    """Handle successful checkout session"""
    try:
        user_id = session.get('client_reference_id')
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')
        
        if not user_id:
            app.logger.error("No client_reference_id found in checkout session")
            return
        
        # Update user with Stripe customer ID
        supabase.table('users').update({
            'stripe_customer_id': customer_id
        }).eq('id', user_id).execute()
        
        app.logger.info(f"Checkout completed for user {user_id}, customer {customer_id}")
        
    except Exception as e:
        app.logger.error(f"Error handling checkout completed: {str(e)}")
        raise

def handle_subscription_created(subscription):
    """Handle new subscription creation"""
    try:
        customer_id = subscription['customer']
        subscription_id = subscription['id']
        status = subscription['status']
        current_period_start = datetime.fromtimestamp(subscription['current_period_start'])
        current_period_end = datetime.fromtimestamp(subscription['current_period_end'])
        
        # Get plan type from metadata
        metadata = subscription.get('metadata', {})
        plan_type = metadata.get('plan_type', 'unknown')
        billing_period = metadata.get('billing_period', 'monthly')
        
        # Find user by customer ID
        user_response = supabase.table('users').select('id').eq('stripe_customer_id', customer_id).execute()
        
        if not user_response.data or len(user_response.data) == 0:
            app.logger.error(f"User not found for customer {customer_id}")
            return
        
        user_id = user_response.data[0]['id']
        
        # Insert subscription
        supabase.table('subscriptions').insert({
            'user_id': user_id,
            'stripe_subscription_id': subscription_id,
            'stripe_customer_id': customer_id,
            'plan_type': plan_type,
            'billing_period': billing_period,
            'status': status,
            'current_period_start': current_period_start.isoformat(),
            'current_period_end': current_period_end.isoformat()
        }).execute()
        
        app.logger.info(f"Subscription created: {subscription_id} for user {user_id}")
        
    except Exception as e:
        app.logger.error(f"Error handling subscription created: {str(e)}")
        raise

def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    try:
        subscription_id = subscription['id']
        status = subscription['status']
        current_period_start = datetime.fromtimestamp(subscription['current_period_start'])
        current_period_end = datetime.fromtimestamp(subscription['current_period_end'])
        
        # Get cancellation date if canceled
        canceled_at = None
        if subscription.get('canceled_at'):
            canceled_at = datetime.fromtimestamp(subscription['canceled_at']).isoformat()
        
        # Update subscription
        update_data = {
            'status': status,
            'current_period_start': current_period_start.isoformat(),
            'current_period_end': current_period_end.isoformat()
        }
        
        if canceled_at:
            update_data['canceled_at'] = canceled_at
        
        supabase.table('subscriptions').update(update_data).eq('stripe_subscription_id', subscription_id).execute()
        
        app.logger.info(f"Subscription updated: {subscription_id}, status: {status}")
        
    except Exception as e:
        app.logger.error(f"Error handling subscription updated: {str(e)}")
        raise

def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    try:
        subscription_id = subscription['id']
        canceled_at = datetime.fromtimestamp(subscription.get('canceled_at', subscription['current_period_end']))
        
        # Update subscription status
        supabase.table('subscriptions').update({
            'status': 'canceled',
            'canceled_at': canceled_at.isoformat()
        }).eq('stripe_subscription_id', subscription_id).execute()
        
        app.logger.info(f"Subscription canceled: {subscription_id}")
        
    except Exception as e:
        app.logger.error(f"Error handling subscription deleted: {str(e)}")
        raise

def handle_invoice_payment_succeeded(invoice):
    """Handle successful invoice payment"""
    try:
        customer_id = invoice['customer']
        subscription_id = invoice.get('subscription')
        amount_paid = invoice['amount_paid'] / 100  # Convert from cents
        
        app.logger.info(f"Payment succeeded for customer {customer_id}, amount: ${amount_paid}")
        
        # You can add logic here to send receipt emails, etc.
        
    except Exception as e:
        app.logger.error(f"Error handling payment succeeded: {str(e)}")
        raise

def handle_invoice_payment_failed(invoice):
    """Handle failed invoice payment"""
    try:
        customer_id = invoice['customer']
        subscription_id = invoice.get('subscription')
        
        # Update subscription status to past_due
        if subscription_id:
            supabase.table('subscriptions').update({
                'status': 'past_due'
            }).eq('stripe_subscription_id', subscription_id).execute()
        
        app.logger.warning(f"Payment failed for customer {customer_id}")
        
        # You can add logic here to send payment failure emails, etc.
        
    except Exception as e:
        app.logger.error(f"Error handling payment failed: {str(e)}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'webhook_server'}), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'service': 'Nexus SEO Webhook Server',
        'status': 'running',
        'endpoints': {
            'webhook': '/webhook (POST)',
            'health': '/health (GET)'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
