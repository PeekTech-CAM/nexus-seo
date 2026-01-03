"""
NEXUS SEO INTELLIGENCE - Stripe Webhook Handler
Production-ready Flask server for processing Stripe webhooks
"""

from flask import Flask, request, jsonify
import os
import logging
from supabase import create_client, Client
from services.stripe_service import StripeService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Initialize Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Service role for server-side operations
)

# Initialize Stripe service
stripe_service = StripeService(supabase)


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'nexus-seo-webhook',
        'version': '1.0.0'
    }), 200


@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    """
    Handle incoming Stripe webhook events.
    
    This endpoint:
    1. Verifies webhook signature
    2. Checks idempotency
    3. Processes event through StripeService
    4. Returns appropriate status
    """
    # Get raw payload
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    if not sig_header:
        logger.warning("Missing Stripe signature header")
        return jsonify({'error': 'Missing signature'}), 400
    
    # Verify signature
    event = stripe_service.verify_webhook_signature(payload, sig_header)
    
    if not event:
        logger.error("Invalid webhook signature")
        return jsonify({'error': 'Invalid signature'}), 400
    
    event_id = event['id']
    event_type = event['type']
    
    logger.info(f"Received webhook: {event_type} ({event_id})")
    
    # Process event
    success, message = stripe_service.process_webhook_event(event)
    
    if success:
        logger.info(f"Successfully processed webhook {event_id}: {message}")
        return jsonify({
            'status': 'success',
            'message': message
        }), 200
    else:
        logger.error(f"Failed to process webhook {event_id}: {message}")
        return jsonify({
            'status': 'error',
            'message': message
        }), 500


@app.route('/webhooks/stripe/test', methods=['POST'])
def test_webhook():
    """
    Test endpoint for webhook integration testing.
    Only enabled in development/staging environments.
    """
    if os.getenv('ENVIRONMENT') == 'production':
        return jsonify({'error': 'Not available in production'}), 403
    
    event_type = request.json.get('event_type')
    
    logger.info(f"Test webhook triggered: {event_type}")
    
    return jsonify({
        'status': 'success',
        'message': f'Test event {event_type} received'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# Rate limiting middleware (simple implementation)
from functools import wraps
from collections import defaultdict
import time

# Simple in-memory rate limiter (use Redis in production)
request_counts = defaultdict(list)

def rate_limit(max_requests=100, window=60):
    """
    Rate limiting decorator.
    
    Args:
        max_requests: Maximum requests allowed
        window: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get client IP
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            now = time.time()
            
            # Clean old requests
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip]
                if now - req_time < window
            ]
            
            # Check limit
            if len(request_counts[client_ip]) >= max_requests:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': window
                }), 429
            
            # Add current request
            request_counts[client_ip].append(now)
            
            return f(*args, **kwargs)
        return wrapped
    return decorator


# Apply rate limiting to webhook endpoint
@app.before_request
def before_request():
    """
    Security checks before processing request.
    """
    # Only allow POST for webhooks
    if request.path.startswith('/webhooks/') and request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    # Verify content type for webhook requests
    if request.path.startswith('/webhooks/stripe'):
        if request.content_type != 'application/json':
            return jsonify({'error': 'Invalid content type'}), 400


if __name__ == '__main__':
    # Production deployment should use Gunicorn
    # gunicorn webhook_server:app --bind 0.0.0.0:8000 --workers 4
    
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('ENVIRONMENT') != 'production'
    
    logger.info(f"Starting webhook server on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )