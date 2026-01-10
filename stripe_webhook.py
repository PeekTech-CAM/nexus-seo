# stripe_webhook.py
import stripe
from supabase import create_client
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Stripe webhook secret from stripe listen
endpoint_secret = "whsec_34edfdf1441d0af35228e2a64eb95d5cf28a369a9303615aa93d9e8ce30adead"

def mark_paid(user_email, plan_name):
    supabase.table("profiles").update({
        "paid": True,
        "plan": plan_name
    }).eq("email", user_email).execute()

@app.route("/stripe_webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({"error": str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({"error": str(e)}), 400

    # Handle the checkout session completion
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        plan_name = session.get("metadata", {}).get("plan_name", "Pro Mensual")
        
        if customer_email:
            mark_paid(customer_email, plan_name)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=8501)
