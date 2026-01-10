"""
Stripe Webhook Handler
This is a separate Flask server that handles Stripe webhooks
Run this separately from your Streamlit app

Usage:
    python webhook.py
"""

from flask import Flask, request, jsonify
import stripe
import os
from supabase import create_client
from datetime import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Try to load from .streamlit/secrets.toml first
def load_secrets():
    """Load secrets from secrets.toml or environment variables"""
    secrets = {}
    
    # Try to load from secrets.toml
    secrets_path = Path(".streamlit/secrets.toml")
    if secrets_path.exists():
        try:
            import toml
            config = toml.load(secrets_path)
            secrets['STRIPE_SECRET_KEY'] = config.get('STRIPE_SECRET_KEY')
            secrets['STRIPE_WEBHOOK_SECRET'] = config.get('STRIPE_WEBHOOK_SECRET')
            secrets['SUPABASE_URL'] = config.get('SUPABASE_URL')
            secrets['SUPABASE_KEY'] = config.get('SUPABASE_KEY')
            logger.info("✅ Loaded secrets from secrets.toml")
            return secrets
        except Exception as e:
            logger.warning(f"Could not load secrets.toml: {e}")
    
    # Fallback to environment variables
    secrets['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')
    secrets['STRIPE_WEBHOOK_SECRET'] = os.getenv('STRIPE_WEBHOOK_SECRET')
    secrets['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    secrets['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')
    
    if any(v is None for v in secrets.values()):
        logger.error("❌ Missing required secrets!")
        logger.error("Set them in .streamlit/secrets.toml or environment variables")
        return None
    
    logger.info("✅ Loaded secrets from environment variables")
    return secrets

# Load configuration
config = load_secrets()
if not config:
    logger.error("Failed to load configuration. Exiting.")
    exit(1)

STRIPE_SECRET_KEY = config['STRIPE_SECRET_KEY']
STRIPE_WEBHOOK_SECRET = config['STRIPE_WEBHOOK_SECRET']
SUPABASE_URL = config['SUPABASE_URL']
SUPABASE_KEY = config['SUPABASE_KEY']

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY
logger.info("✅ Stripe initialized")

# Initialize Supabase
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Supabase: {e}")
    exit(1)

def update_user_subscription(customer_id, subscription_id, status, tier):
    """Update user subscription in database"""
    try:
        # Find user by stripe_customer_id
        response = supabase.table('profiles')\
            .select('*')\
            .eq('stripe_customer_id', customer_id)\
            .single()\
            .execute()
        
        if response.data:
            user_id = response.data['id']
            
            # Update subscription info
            update_data = {
                'stripe_subscription_id': subscription_id,
                'subscription_status': status,
                'tier': tier,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            # Set limits based on tier
            if tier == 'pro':
                update_data['monthly_scan_limit'] = 50
                update_data['credits_balance'] = update_data.get('credits_balance', 0) + 10000
            elif tier == 'agency':
                update_data['monthly_scan_limit'] = 200
                update_data['credits_balance'] = update_data.get('credits_balance', 0) + 50000
            elif tier == 'elite':
                update_data['monthly_scan_limit'] = 999999  # Unlimited
                update_data['credits_balance'] = update_data.get('credits_balance', 0) + 200000
            
            supabase.table('profiles')\
                .update(update_data)\
                .eq('id', user_id)\
                .execute()
            
            logger.info(f"Updated subscription for user {user_id}: {tier} - {status}")
            return True
        else:
            logger.warning(f"User not found for customer_id: {customer_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error updating subscription: {e}")
        return False

def add_credits_to_user(customer_id, credits):
    """Add credits to user account"""
    try:
        # Find user by stripe_customer_id
        response = supabase.table('profiles')\
            .select('*')\
            .eq('stripe_customer_id', customer_id)\
            .single()\
            .execute()
        
        if response.data:
            user_id = response.data['id']
            current_credits = response.data.get('credits_balance', 0)
            new_credits = current_credits + credits
            
            supabase.table('profiles')\
                .update({
                    'credits_balance': new_credits,
                    'updated_at': datetime.utcnow().isoformat()
                })\
                .eq('id', user_id)\
                .execute()
            
            logger.info(f"Added {credits} credits to user {user_id}. New balance: {new_credits}")
            return True
        else:
            logger.warning(f"User not found for customer_id: {customer_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error adding credits: {e}")
        return False

def create_stripe_customer_if_needed(user_id, email):
    """Create Stripe customer if user doesn't have one"""
    try:
        # Check if user already has a customer ID
        response = supabase.table('profiles')\
            .select('stripe_customer_id')\
            .eq('id', user_id)\
            .single()\
            .execute()
        
        if response.data and response.data.get('stripe_customer_id'):
            return response.data['stripe_customer_id']
        
        # Create new Stripe customer
        customer = stripe.Customer.create(
            email=email,
            metadata={'user_id': user_id}
        )
        
        # Update database
        supabase.table('profiles')\
            .update({'stripe_customer_id': customer.id})\
            .eq('id', user_id)\
            .execute()
        
        logger.info(f"Created Stripe customer {customer.id} for user {user_id}")
        return customer.id
        
    except Exception as e:
        logger.error(f"Error creating Stripe customer: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhook events"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        
        logger.info(f"Received event: {event['type']}")
        
        # Handle different event types
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            handle_checkout_completed(session)
        
        elif event['type'] == 'customer.subscription.created':
            subscription = event['data']['object']
            handle_subscription_created(subscription)
        
        elif event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            handle_subscription_updated(subscription)
        
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            handle_subscription_deleted(subscription)
        
        elif event['type'] == 'invoice.payment_succeeded':
            invoice = event['data']['object']
            handle_invoice_paid(invoice)
        
        elif event['type'] == 'invoice.payment_failed':
            invoice = event['data']['object']
            handle_invoice_failed(invoice)
        
        elif event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            handle_payment_succeeded(intent)
        
        else:
            logger.info(f"Unhandled event type: {event['type']}")
        
        return jsonify({'status': 'success'}), 200
        
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return jsonify({'error': 'Invalid payload'}), 400
    
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return jsonify({'error': 'Invalid signature'}), 400
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

def handle_checkout_completed(session):
    """Handle completed checkout session"""
    customer_id = session.get('customer')
    client_reference_id = session.get('client_reference_id')  # This is the user_id
    mode = session.get('mode')
    metadata = session.get('metadata', {})
    
    logger.info(f"Checkout completed for customer {customer_id}, user {client_reference_id}")
    
    # Update user with customer ID if not already set
    if client_reference_id and customer_id:
        try:
            supabase.table('profiles')\
                .update({'stripe_customer_id': customer_id})\
                .eq('id', client_reference_id)\
                .execute()
        except Exception as e:
            logger.error(f"Error updating customer ID: {e}")
    
    # Handle credit pack purchases (one-time payments)
    if mode == 'payment':
        credits = int(metadata.get('credits', 0))
        if credits > 0 and customer_id:
            add_credits_to_user(customer_id, credits)

def handle_subscription_created(subscription):
    """Handle new subscription"""
    customer_id = subscription['customer']
    subscription_id = subscription['id']
    status = subscription['status']
    metadata = subscription.get('metadata', {})
    tier = metadata.get('tier', 'pro')
    
    logger.info(f"Subscription created: {subscription_id} for customer {customer_id}")
    
    if status == 'active':
        update_user_subscription(customer_id, subscription_id, status, tier)

def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    customer_id = subscription['customer']
    subscription_id = subscription['id']
    status = subscription['status']
    metadata = subscription.get('metadata', {})
    tier = metadata.get('tier', 'pro')
    
    logger.info(f"Subscription updated: {subscription_id} - {status}")
    
    update_user_subscription(customer_id, subscription_id, status, tier)

def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    customer_id = subscription['customer']
    subscription_id = subscription['id']
    
    logger.info(f"Subscription deleted: {subscription_id}")
    
    # Set subscription to canceled
    update_user_subscription(customer_id, subscription_id, 'canceled', 'free')

def handle_invoice_paid(invoice):
    """Handle successful invoice payment"""
    customer_id = invoice['customer']
    subscription_id = invoice.get('subscription')
    
    logger.info(f"Invoice paid for customer {customer_id}")
    
    # If it's a subscription renewal, add credits
    if subscription_id:
        subscription = stripe.Subscription.retrieve(subscription_id)
        metadata = subscription.get('metadata', {})
        tier = metadata.get('tier', 'pro')
        
        # Add monthly credits based on tier
        if tier == 'pro':
            add_credits_to_user(customer_id, 10000)
        elif tier == 'agency':
            add_credits_to_user(customer_id, 50000)
        elif tier == 'elite':
            add_credits_to_user(customer_id, 200000)

def handle_invoice_failed(invoice):
    """Handle failed invoice payment"""
    customer_id = invoice['customer']
    
    logger.warning(f"Invoice payment failed for customer {customer_id}")
    
    # Optionally: send email notification, update user status, etc.

def handle_payment_succeeded(intent):
    """Handle successful one-time payment"""
    customer_id = intent.get('customer')
    metadata = intent.get('metadata', {})
    
    logger.info(f"Payment succeeded for customer {customer_id}")
    
    # Handle credit pack purchases
    credits = int(metadata.get('credits', 0))
    if credits > 0 and customer_id:
        add_credits_to_user(customer_id, credits)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 Starting Nexus SEO Webhook Server")
    logger.info("=" * 60)
    logger.info(f"📍 Webhook endpoint: http://localhost:5000/webhook")
    logger.info(f"💚 Health check: http://localhost:5000/health")
    logger.info("=" * 60)
    
    # Run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)