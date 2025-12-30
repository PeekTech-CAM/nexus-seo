# webhook_server.py
from fastapi import FastAPI, Request, HTTPException
import stripe
import os
from supabase import create_client, Client

# Load environment variables
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

stripe.api_key = STRIPE_API_KEY

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        # Add credits to user
        user = supabase.table("profiles").select("*").eq("email", customer_email).single().execute().data
        if user:
            new_credits = user.get("credits", 0) + 500  # Add 500 credits per purchase
            supabase.table("profiles").update({"credits": new_credits}).eq("email", customer_email).execute()
            print(f"Added 500 credits to {customer_email}")

    return {"status": "success"}