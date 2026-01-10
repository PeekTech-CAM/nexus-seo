import stripe
import os
import sqlite3
from datetime import datetime

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

def handle_webhook(payload, sig_header):
    """
    Handle incoming Stripe webhook events
    
    Args:
        payload: The raw request body
        sig_header: The Stripe-Signature header
    
    Returns:
        dict: Response indicating success or failure
    """
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return {'error': 'Invalid payload', 'status': 400}
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return {'error': 'Invalid signature', 'status': 400}
    
    # Handle the event
    event_type = event['type']
    
    if event_type == 'checkout.session.completed':
        return handle_checkout_completed(event['data']['object'])
    
    elif event_type == 'customer.subscription.created':
        return handle_subscription_created(event['data']['object'])
    
    elif event_type == 'customer.subscription.updated':
        return handle_subscription_updated(event['data']['object'])
    
    elif event_type == 'customer.subscription.deleted':
        return handle_subscription_deleted(event['data']['object'])
    
    elif event_type == 'invoice.payment_succeeded':
        return handle_invoice_payment_succeeded(event['data']['object'])
    
    elif event_type == 'invoice.payment_failed':
        return handle_invoice_payment_failed(event['data']['object'])
    
    else:
        # Unhandled event type
        return {'message': f'Unhandled event type: {event_type}', 'status': 200}

def handle_checkout_completed(session):
    """Handle successful checkout session"""
    try:
        user_id = session.get('client_reference_id')
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')
        
        if not user_id:
            return {'error': 'No client_reference_id found', 'status': 400}
        
        # Update user with Stripe customer ID
        conn = sqlite3.connect('nexus_seo.db')
        c = conn.cursor()
        
        c.execute('''
            UPDATE users 
            SET stripe_customer_id = ? 
            WHERE id = ?
        ''', (customer_id, user_id))
        
        conn.commit()
        conn.close()
        
        return {'message': 'Checkout completed successfully', 'status': 200}
    
    except Exception as e:
        return {'error': str(e), 'status': 500}

def handle_subscription_created(subscription):
    """Handle new subscription creation"""
    try:
        customer_id = subscription['customer']
        subscription_id = subscription['id']
        status = subscription['status']
        current_period_start = datetime.fromtimestamp(subscription['current_period_start'])
        current_period_end = datetime.fromtimestamp(subscription['current_period_end'])
        
        # Get plan type from metadata or price
        plan_type = subscription.get('metadata', {}).get('plan_type', 'unknown')
        
        # Find user by customer ID
        conn = sqlite3.connect('nexus_seo.db')
        c = conn.cursor()
        
        c.execute('SELECT id FROM users WHERE stripe_customer_id = ?', (customer_id,))
        user = c.fetchone()
        
        if not user:
            conn.close()
            return {'error': 'User not found for customer', 'status': 404}
        
        user_id = user[0]
        
        # Insert or update subscription
        c.execute('''
            INSERT INTO subscriptions 
            (user_id, stripe_subscription_id, stripe_customer_id, plan_type, status, 
             current_period_start, current_period_end)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(stripe_subscription_id) 
            DO UPDATE SET 
                status = excluded.status,
                current_period_start = excluded.current_period_start,
                current_period_end = excluded.current_period_end
        ''', (user_id, subscription_id, customer_id, plan_type, status,
              current_period_start, current_period_end))
        
        conn.commit()
        conn.close()
        
        return {'message': 'Subscription created successfully', 'status': 200}
    
    except Exception as e:
        return {'error': str(e), 'status': 500}

def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    try:
        subscription_id = subscription['id']
        status = subscription['status']
        current_period_start = datetime.fromtimestamp(subscription['current_period_start'])
        current_period_end = datetime.fromtimestamp(subscription['current_period_end'])
        
        # Update subscription in database
        conn = sqlite3.connect('nexus_seo.db')
        c = conn.cursor()
        
        c.execute('''
            UPDATE subscriptions
            SET status = ?,
                current_period_start = ?,
                current_period_end = ?
            WHERE stripe_subscription_id = ?
        ''', (status, current_period_start, current_period_end, subscription_id))
        
        conn.commit()
        conn.close()
        
        return {'message': 'Subscription updated successfully', 'status': 200}
    
    except Exception as e:
        return {'error': str(e), 'status': 500}

def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    try:
        subscription_id = subscription['id']
        
        # Update subscription status to canceled
        conn = sqlite3.connect('nexus_seo.db')
        c = conn.cursor()
        
        c.execute('''
            UPDATE subscriptions
            SET status = 'canceled'
            WHERE stripe_subscription_id = ?
        ''', (subscription_id,))
        
        conn.commit()
        conn.close()
        
        return {'message': 'Subscription canceled successfully', 'status': 200}
    
    except Exception as e:
        return {'error': str(e), 'status': 500}

def handle_invoice_payment_succeeded(invoice):
    """Handle successful invoice payment"""
    try:
        customer_id = invoice['customer']
        subscription_id = invoice.get('subscription')
        
        # Log successful payment
        # You can add additional logic here like sending confirmation emails
        
        return {'message': 'Payment succeeded', 'status': 200}
    
    except Exception as e:
        return {'error': str(e), 'status': 500}

def handle_invoice_payment_failed(invoice):
    """Handle failed invoice payment"""
    try:
        customer_id = invoice['customer']
        subscription_id = invoice.get('subscription')
        
        # Log failed payment
        # You can add logic here to notify the user or update subscription status
        
        # Optionally update subscription status
        if subscription_id:
            conn = sqlite3.connect('nexus_seo.db')
            c = conn.cursor()
            
            c.execute('''
                UPDATE subscriptions
                SET status = 'past_due'
                WHERE stripe_subscription_id = ?
            ''', (subscription_id,))
            
            conn.commit()
            conn.close()
        
        return {'message': 'Payment failed handled', 'status': 200}
    
    except Exception as e:
        return {'error': str(e), 'status': 500}