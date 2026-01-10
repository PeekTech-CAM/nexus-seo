"""
NEXUS SEO INTELLIGENCE - Stripe Billing Service
Production-grade subscription management with Stripe
"""

import os
import stripe
import hmac
import hashlib
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from supabase import Client
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Stripe configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Pricing configuration (Price IDs from Stripe Dashboard)
PRICING_CONFIG = {
    'pro': {
        'monthly': {
            'price_id': os.getenv('STRIPE_PRICE_PRO_MONTHLY'),
            'amount': 4900,  # $49.00
            'credits': 5000,
            'scan_limit': 50
        },
        'yearly': {
            'price_id': os.getenv('STRIPE_PRICE_PRO_YEARLY'),
            'amount': 47000,  # $470.00 (saves $118)
            'credits': 60000,  # 12 months worth
            'scan_limit': 600
        }
    },
    'agency': {
        'monthly': {
            'price_id': os.getenv('STRIPE_PRICE_AGENCY_MONTHLY'),
            'amount': 14900,
            'credits': 20000,
            'scan_limit': 200
        },
        'yearly': {
            'price_id': os.getenv('STRIPE_PRICE_AGENCY_YEARLY'),
            'amount': 143000,
            'credits': 240000,
            'scan_limit': 2400
        }
    },
    'elite': {
        'monthly': {
            'price_id': os.getenv('STRIPE_PRICE_ELITE_MONTHLY'),
            'amount': 39900,
            'credits': 100000,
            'scan_limit': 999999  # Effectively unlimited
        }
    }
}


class StripeService:
    """
    Handles all Stripe billing operations including:
    - Checkout session creation
    - Webhook event processing
    - Subscription management
    - Customer portal access
    """
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.base_url = os.getenv('APP_BASE_URL', 'http://localhost:8501')
    
    def create_checkout_session(
        self,
        user_id: str,
        email: str,
        tier: str,
        interval: str = 'month'
    ) -> Dict[str, str]:
        """
        Create a Stripe Checkout session for new subscription.
        
        Args:
            user_id: Supabase user ID
            email: User's email address
            tier: Subscription tier (pro, agency, elite)
            interval: Billing interval (month, year)
        
        Returns:
            Dict containing checkout_url and session_id
        
        Raises:
            ValueError: If tier/interval combination is invalid
            stripe.error.StripeError: If Stripe API fails
        """
        try:
            # Validate tier and interval
            if tier not in PRICING_CONFIG:
                raise ValueError(f"Invalid tier: {tier}")
            
            if interval not in PRICING_CONFIG[tier]:
                raise ValueError(f"Invalid interval for {tier}: {interval}")
            
            price_id = PRICING_CONFIG[tier][interval]['price_id']
            
            if not price_id:
                raise ValueError(f"Price ID not configured for {tier}/{interval}")
            
            # Get or create Stripe customer
            customer_id = self._get_or_create_customer(user_id, email)
            
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{self.base_url}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{self.base_url}/billing/cancelled",
                
                # Metadata for webhook processing
                metadata={
                    'user_id': user_id,
                    'tier': tier,
                    'interval': interval
                },
                
                # Subscription configuration
                subscription_data={
                    'metadata': {
                        'user_id': user_id,
                        'tier': tier
                    },
                    'trial_period_days': 14 if interval == 'month' else None,
                },
                
                # Allow promotional codes
                allow_promotion_codes=True,
                
                # Tax calculation
                automatic_tax={'enabled': True},
            )
            
            logger.info(f"Created checkout session for user {user_id}: {session.id}")
            
            return {
                'checkout_url': session.url,
                'session_id': session.id
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            raise
    
    def _get_or_create_customer(self, user_id: str, email: str) -> str:
        """
        Get existing Stripe customer ID or create new customer.
        """
        try:
            # Check if user already has Stripe customer
            profile = self.supabase.table('profiles').select('stripe_customer_id').eq('id', user_id).single().execute()
            
            if profile.data and profile.data.get('stripe_customer_id'):
                return profile.data['stripe_customer_id']
            
            # Create new Stripe customer
            customer = stripe.Customer.create(
                email=email,
                metadata={'user_id': user_id}
            )
            
            # Store customer ID in database
            self.supabase.table('profiles').update({
                'stripe_customer_id': customer.id
            }).eq('id', user_id).execute()
            
            logger.info(f"Created Stripe customer for user {user_id}: {customer.id}")
            
            return customer.id
            
        except Exception as e:
            logger.error(f"Error getting/creating customer: {e}")
            raise
    
    def create_portal_session(self, user_id: str) -> str:
        """
        Create Stripe Customer Portal session for subscription management.
        
        Returns:
            Portal URL for redirection
        """
        try:
            # Get customer ID
            profile = self.supabase.table('profiles').select('stripe_customer_id').eq('id', user_id).single().execute()
            
            if not profile.data or not profile.data.get('stripe_customer_id'):
                raise ValueError("User does not have a Stripe customer")
            
            customer_id = profile.data['stripe_customer_id']
            
            # Create portal session
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=f"{self.base_url}/billing"
            )
            
            logger.info(f"Created portal session for user {user_id}")
            
            return session.url
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating portal: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating portal session: {e}")
            raise
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> Optional[Dict]:
        """
        Verify Stripe webhook signature and return event.
        
        Args:
            payload: Raw webhook payload bytes
            signature: Stripe-Signature header value
        
        Returns:
            Parsed Stripe event or None if verification fails
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            logger.error(f"Invalid webhook payload: {e}")
            return None
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {e}")
            return None
    
    def process_webhook_event(self, event: Dict) -> Tuple[bool, str]:
        """
        Process Stripe webhook event with idempotency.
        
        Args:
            event: Stripe event object
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        event_id = event['id']
        event_type = event['type']
        
        try:
            # Check if event already processed (idempotency)
            existing = self.supabase.table('stripe_events').select('*').eq('id', event_id).execute()
            
            if existing.data and existing.data[0].get('processed'):
                logger.info(f"Event {event_id} already processed, skipping")
                return True, "Event already processed"
            
            # Store event for idempotency tracking
            self.supabase.table('stripe_events').upsert({
                'id': event_id,
                'type': event_type,
                'data': event,
                'processed': False,
                'created_at': datetime.utcnow().isoformat()
            }).execute()
            
            # Route to appropriate handler
            handler_map = {
                'checkout.session.completed': self._handle_checkout_completed,
                'customer.subscription.updated': self._handle_subscription_updated,
                'customer.subscription.deleted': self._handle_subscription_deleted,
                'invoice.paid': self._handle_invoice_paid,
                'invoice.payment_failed': self._handle_payment_failed,
            }
            
            handler = handler_map.get(event_type)
            
            if handler:
                success, message = handler(event['data']['object'])
                
                if success:
                    # Mark event as processed
                    self.supabase.table('stripe_events').update({
                        'processed': True,
                        'processed_at': datetime.utcnow().isoformat()
                    }).eq('id', event_id).execute()
                    
                    logger.info(f"Successfully processed event {event_id}: {event_type}")
                    return True, message
                else:
                    logger.error(f"Failed to process event {event_id}: {message}")
                    return False, message
            else:
                logger.info(f"Unhandled event type: {event_type}")
                return True, "Event type not handled"
                
        except Exception as e:
            logger.error(f"Error processing webhook event {event_id}: {e}")
            
            # Increment retry count
            self.supabase.table('stripe_events').update({
                'retry_count': self.supabase.rpc('increment', {'x': 1}),
                'error_message': str(e)
            }).eq('id', event_id).execute()
            
            return False, str(e)
    
    def _handle_checkout_completed(self, session: Dict) -> Tuple[bool, str]:
        """
        Handle successful checkout completion.
        Creates subscription record and grants initial credits.
        """
        try:
            user_id = session['metadata']['user_id']
            tier = session['metadata']['tier']
            interval = session['metadata']['interval']
            
            subscription_id = session['subscription']
            customer_id = session['customer']
            
            # Retrieve full subscription details from Stripe
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Get pricing config
            pricing = PRICING_CONFIG[tier][interval]
            
            # Create subscription record
            self.supabase.table('subscriptions').insert({
                'user_id': user_id,
                'stripe_subscription_id': subscription_id,
                'stripe_customer_id': customer_id,
                'stripe_price_id': subscription['items']['data'][0]['price']['id'],
                'status': subscription['status'],
                'tier': tier,
                'currency': subscription['currency'],
                'amount': pricing['amount'],
                'interval': interval,
                'current_period_start': datetime.fromtimestamp(subscription['current_period_start']).isoformat(),
                'current_period_end': datetime.fromtimestamp(subscription['current_period_end']).isoformat(),
                'trial_start': datetime.fromtimestamp(subscription['trial_start']).isoformat() if subscription.get('trial_start') else None,
                'trial_end': datetime.fromtimestamp(subscription['trial_end']).isoformat() if subscription.get('trial_end') else None,
            }).execute()
            
            # Update user profile
            self.supabase.table('profiles').update({
                'tier': tier,
                'stripe_subscription_id': subscription_id,
                'monthly_scan_limit': pricing['scan_limit'],
                'tier_updated_at': datetime.utcnow().isoformat()
            }).eq('id', user_id).execute()
            
            # Grant initial credits
            self._grant_credits(
                user_id=user_id,
                amount=pricing['credits'],
                reference_id=subscription_id,
                reference_type='subscription',
                description=f"Initial credits for {tier.title()} {interval}ly subscription"
            )
            
            # Create audit log
            self._create_audit_log(
                user_id=user_id,
                action='subscription_created',
                resource_type='subscription',
                resource_id=subscription_id,
                metadata={
                    'tier': tier,
                    'interval': interval,
                    'amount': pricing['amount']
                }
            )
            
            return True, "Checkout completed successfully"
            
        except Exception as e:
            logger.error(f"Error handling checkout completion: {e}")
            return False, str(e)
    
    def _handle_subscription_updated(self, subscription: Dict) -> Tuple[bool, str]:
        """
        Handle subscription updates (plan changes, renewals, etc.)
        """
        try:
            user_id = subscription['metadata']['user_id']
            subscription_id = subscription['id']
            
            # Update subscription record
            self.supabase.table('subscriptions').update({
                'status': subscription['status'],
                'current_period_start': datetime.fromtimestamp(subscription['current_period_start']).isoformat(),
                'current_period_end': datetime.fromtimestamp(subscription['current_period_end']).isoformat(),
                'cancel_at_period_end': subscription['cancel_at_period_end'],
                'canceled_at': datetime.fromtimestamp(subscription['canceled_at']).isoformat() if subscription.get('canceled_at') else None,
            }).eq('stripe_subscription_id', subscription_id).execute()
            
            return True, "Subscription updated successfully"
            
        except Exception as e:
            logger.error(f"Error handling subscription update: {e}")
            return False, str(e)
    
    def _handle_subscription_deleted(self, subscription: Dict) -> Tuple[bool, str]:
        """
        Handle subscription cancellation/deletion.
        Downgrade user to demo tier.
        """
        try:
            user_id = subscription['metadata']['user_id']
            subscription_id = subscription['id']
            
            # Update subscription status
            self.supabase.table('subscriptions').update({
                'status': 'canceled',
                'ended_at': datetime.utcnow().isoformat()
            }).eq('stripe_subscription_id', subscription_id).execute()
            
            # Downgrade user to demo tier
            self.supabase.table('profiles').update({
                'tier': 'demo',
                'monthly_scan_limit': 2,
                'tier_updated_at': datetime.utcnow().isoformat()
            }).eq('id', user_id).execute()
            
            # Create audit log
            self._create_audit_log(
                user_id=user_id,
                action='subscription_canceled',
                resource_type='subscription',
                resource_id=subscription_id
            )
            
            return True, "Subscription canceled successfully"
            
        except Exception as e:
            logger.error(f"Error handling subscription deletion: {e}")
            return False, str(e)
    
    def _handle_invoice_paid(self, invoice: Dict) -> Tuple[bool, str]:
        """
        Handle successful invoice payment.
        Grant monthly credits on renewal.
        """
        try:
            subscription_id = invoice.get('subscription')
            
            if not subscription_id:
                return True, "No subscription associated with invoice"
            
            # Get subscription details
            sub_record = self.supabase.table('subscriptions').select('*').eq('stripe_subscription_id', subscription_id).single().execute()
            
            if not sub_record.data:
                return False, "Subscription record not found"
            
            user_id = sub_record.data['user_id']
            tier = sub_record.data['tier']
            interval = sub_record.data['interval']
            
            # Grant renewal credits
            pricing = PRICING_CONFIG[tier][interval]
            self._grant_credits(
                user_id=user_id,
                amount=pricing['credits'],
                reference_id=subscription_id,
                reference_type='subscription',
                description=f"Monthly renewal credits for {tier.title()} subscription"
            )
            
            # Reset monthly scan counter
            self.supabase.table('profiles').update({
                'monthly_scans_used': 0,
                'scan_limit_reset_date': datetime.utcnow() + timedelta(days=30)
            }).eq('id', user_id).execute()
            
            return True, "Invoice paid and credits granted"
            
        except Exception as e:
            logger.error(f"Error handling invoice paid: {e}")
            return False, str(e)
    
    def _handle_payment_failed(self, invoice: Dict) -> Tuple[bool, str]:
        """
        Handle failed payment.
        Send notification and potentially downgrade after grace period.
        """
        try:
            subscription_id = invoice.get('subscription')
            
            if not subscription_id:
                return True, "No subscription associated with invoice"
            
            # Update subscription status
            self.supabase.table('subscriptions').update({
                'status': 'past_due'
            }).eq('stripe_subscription_id', subscription_id).execute()
            
            # TODO: Send payment failed email
            # TODO: Implement grace period logic before downgrade
            
            return True, "Payment failure handled"
            
        except Exception as e:
            logger.error(f"Error handling payment failure: {e}")
            return False, str(e)
    
    def _grant_credits(
        self,
        user_id: str,
        amount: int,
        reference_id: str,
        reference_type: str,
        description: str
    ):
        """
        Grant credits to user and create transaction record.
        """
        try:
            # Get current balance
            profile = self.supabase.table('profiles').select('credits_balance').eq('id', user_id).single().execute()
            current_balance = profile.data['credits_balance']
            new_balance = current_balance + amount
            
            # Update profile
            self.supabase.table('profiles').update({
                'credits_balance': new_balance,
                'total_credits_purchased': self.supabase.rpc('increment', {'x': amount})
            }).eq('id', user_id).execute()
            
            # Create transaction record
            self.supabase.table('credit_transactions').insert({
                'user_id': user_id,
                'type': 'subscription_credit',
                'amount': amount,
                'balance_after': new_balance,
                'reference_id': reference_id,
                'reference_type': reference_type,
                'description': description
            }).execute()
            
            logger.info(f"Granted {amount} credits to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error granting credits: {e}")
            raise
    
    def _create_audit_log(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Create audit log entry for important actions.
        """
        try:
            self.supabase.table('audit_logs').insert({
                'user_id': user_id,
                'action': action,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'metadata': metadata or {}
            }).execute()
        except Exception as e:
            logger.error(f"Error creating audit log: {e}")
            # Don't raise - audit log failure shouldn't block operations
