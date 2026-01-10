import os
import json
import stripe
import streamlit as st
from supabase import create_client, Client

# --- SUPABASE SETUP ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- STRIPE SETUP ---
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

st.title("Stripe Webhook Listener")  # For debugging

# --- FUNCTION TO PROCESS EVENTS ---
def process_event(event):
    type_ = event["type"]
    data = event["data"]["object"]

    if type_ == "checkout.session.completed":
        handle_checkout_session(data)
    elif type_ == "customer.subscription.deleted":
        handle_subscription_deleted(data)
    elif type_ == "invoice.paid":
        # optional auto-renew handling
        pass

# --- HELPER FUNCTIONS ---
def handle_checkout_session(session):
    # Prevent duplicate
    existing = supabase.table("payments").select("*").eq("stripe_event_id", session["id"]).execute()
    if existing.data:
        return

    user_id = session["client_reference_id"]
    amount = session["amount_total"] // 100
    credits = 0

    # Map price_id to credits or tier
    price_id = session["line_items"]["data"][0]["price"]["id"]

    if price_id == os.environ.get("STRIPE_PRICE_CREDITS_1000"):
        credits = 1000
    elif price_id == os.environ.get("STRIPE_PRICE_CREDITS_5000"):
        credits = 5000
    elif price_id == os.environ.get("STRIPE_PRICE_CREDITS_10000"):
        credits = 10000
    else:
        tier = "pro" if "PRO" in price_id.upper() else "agency" if "AGENCY" in price_id.upper() else "elite"
        supabase.table("profiles").update({
            "tier": tier,
            "subscription_status": "active",
            "stripe_subscription_id": session.get("subscription"),
            "current_period_end": session.get("current_period_end")
        }).eq("id", user_id).execute()

    if credits:
        profile = supabase.table("profiles").select("credits_balance").eq("id", user_id).single().execute()
        new_credits = profile.data["credits_balance"] + credits
        supabase.table("profiles").update({"credits_balance": new_credits}).eq("id", user_id).execute()

    supabase.table("payments").insert({
        "user_id": user_id,
        "stripe_event_id": session["id"],
        "type": "checkout.session.completed",
        "amount": amount,
        "credits": credits
    }).execute()

def handle_subscription_deleted(subscription):
    user_id = subscription["metadata"]["user_id"]
    supabase.table("profiles").update({
        "subscription_status": "inactive",
        "tier": "free",
        "stripe_subscription_id": None
    }).eq("id", user_id).execute()

# --- STREAMLIT WEBHOOK LISTENER ---
@st.experimental_singleton
def stripe_listener():
    return st.runtime.scriptrunner.add_event_listener("POST", "/webhook", lambda request: handle_request(request))

def handle_request(request):
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        st.error(f"Webhook error: {str(e)}")
        return {"status": 400}

    process_event(event)
    return {"status": 200}

# Activate listener
stripe_listener()
st.success("Stripe webhook listener active ✅")
