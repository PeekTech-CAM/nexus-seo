import stripe
import os
from supabase import create_client

# Configuration
stripe.api_key = "sk_...................." 
supabase = create_client("sb_.............")
endpoint_secret = "whsec_............" 

def handle_webhook(payload, sig_header):
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return "Error", 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        
        # Determine the plan based on what they bought
        # You get these IDs from your Stripe Product Dashboard
        price_id = session['line_items']['data'][0]['price']['id']
        
        new_plan = "Starter"
        if price_id == "price_PRO_ID": new_plan = "Pro"
        elif price_id == "price_AGENCY_ID": new_plan = "Agency"

        # Update Supabase automatically
        supabase.table("profiles").update({"plan_tier": new_plan, "credits": 999}).eq("email", customer_email).execute()
    
    return "Success", 200