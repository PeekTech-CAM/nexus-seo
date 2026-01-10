"""
Stripe Product Setup Script
Run this once to create all products and prices in Stripe
"""

import stripe
import os
from pathlib import Path

# Try to load from secrets file first
secrets_path = Path(".streamlit/secrets.toml")

if secrets_path.exists():
    print("📝 Reading Stripe key from secrets.toml...")
    import toml
    secrets = toml.load(secrets_path)
    stripe.api_key = secrets.get("STRIPE_SECRET_KEY")
    if not stripe.api_key or stripe.api_key == "sk_test_YOUR_KEY_HERE":
        print("\n❌ ERROR: No valid Stripe key found in secrets.toml")
        print("\n🔧 SETUP REQUIRED:")
        print("1. Go to: https://dashboard.stripe.com/test/apikeys")
        print("2. Copy your 'Secret key' (starts with sk_test_)")
        print("3. Paste it in .streamlit/secrets.toml as STRIPE_SECRET_KEY")
        exit(1)
else:
    print("\n❌ ERROR: secrets.toml not found!")
    print("\n🔧 SETUP REQUIRED:")
    print("1. Create file: .streamlit/secrets.toml")
    print("2. Add your Stripe test key:")
    print('   STRIPE_SECRET_KEY = "sk_test_YOUR_ACTUAL_KEY"')
    print("\n3. Get your key from: https://dashboard.stripe.com/test/apikeys")
    exit(1)

def create_products():
    """Create all Nexus SEO products in Stripe"""
    
    print("🚀 Creating Stripe Products...\n")
    
    # ========================================
    # SUBSCRIPTION PRODUCTS
    # ========================================
    
    try:
        # PRO PLAN
        print("Creating Pro Plan...")
        pro_product = stripe.Product.create(
            name="Nexus SEO - Pro Plan",
            description="Professional SEO analysis with advanced features"
        )
        
        pro_monthly = stripe.Price.create(
            product=pro_product.id,
            unit_amount=4900,  # €49.00
            currency="eur",
            recurring={"interval": "month"}
        )
        print(f"✅ Pro Monthly: {pro_monthly.id}")
        
        pro_annual = stripe.Price.create(
            product=pro_product.id,
            unit_amount=47000,  # €470.00
            currency="eur",
            recurring={"interval": "year"}
        )
        print(f"✅ Pro Annual: {pro_annual.id}\n")
        
    except Exception as e:
        print(f"❌ Error creating Pro Plan: {e}\n")
    
    try:
        # AGENCY PLAN
        print("Creating Agency Plan...")
        agency_product = stripe.Product.create(
            name="Nexus SEO - Agency Plan",
            description="Enterprise-grade SEO tools for agencies"
        )
        
        agency_monthly = stripe.Price.create(
            product=agency_product.id,
            unit_amount=14900,  # €149.00
            currency="eur",
            recurring={"interval": "month"}
        )
        print(f"✅ Agency Monthly: {agency_monthly.id}")
        
        agency_annual = stripe.Price.create(
            product=agency_product.id,
            unit_amount=143000,  # €1,430.00
            currency="eur",
            recurring={"interval": "year"}
        )
        print(f"✅ Agency Annual: {agency_annual.id}\n")
        
    except Exception as e:
        print(f"❌ Error creating Agency Plan: {e}\n")
    
    try:
        # ELITE PLAN
        print("Creating Elite Plan...")
        elite_product = stripe.Product.create(
            name="Nexus SEO - Elite Plan",
            description="Premium unlimited SEO analysis with dedicated support"
        )
        
        elite_monthly = stripe.Price.create(
            product=elite_product.id,
            unit_amount=39900,  # €399.00
            currency="eur",
            recurring={"interval": "month"}
        )
        print(f"✅ Elite Monthly: {elite_monthly.id}")
        
        elite_annual = stripe.Price.create(
            product=elite_product.id,
            unit_amount=430000,  # €4,300.00 (save €488/year)
            currency="eur",
            recurring={"interval": "year"}
        )
        print(f"✅ Elite Annual: {elite_annual.id}\n")
        
    except Exception as e:
        print(f"❌ Error creating Elite Plan: {e}\n")
    
    # ========================================
    # CREDIT PACKS (One-time payments)
    # ========================================
    
    try:
        print("Creating Credit Packs...")
        credits_product = stripe.Product.create(
            name="Nexus SEO - Credits",
            description="One-time credit packs for SEO analysis"
        )
        
        credits_1000 = stripe.Price.create(
            product=credits_product.id,
            unit_amount=1000,  # €10.00
            currency="eur"
        )
        print(f"✅ 1,000 Credits: {credits_1000.id}")
        
        credits_5000 = stripe.Price.create(
            product=credits_product.id,
            unit_amount=4000,  # €40.00
            currency="eur"
        )
        print(f"✅ 5,000 Credits: {credits_5000.id}")
        
        credits_10000 = stripe.Price.create(
            product=credits_product.id,
            unit_amount=7500,  # €75.00
            currency="eur"
        )
        print(f"✅ 10,000 Credits: {credits_10000.id}\n")
        
    except Exception as e:
        print(f"❌ Error creating Credit Packs: {e}\n")
    
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\n📋 Copy these Price IDs to your secrets.toml:\n")
    
    print(f"""
STRIPE_PRICE_PRO_MONTHLY = "{pro_monthly.id}"
STRIPE_PRICE_PRO_ANNUAL = "{pro_annual.id}"
STRIPE_PRICE_AGENCY_MONTHLY = "{agency_monthly.id}"
STRIPE_PRICE_AGENCY_ANNUAL = "{agency_annual.id}"
STRIPE_PRICE_ELITE_MONTHLY = "{elite_monthly.id}"
STRIPE_PRICE_ELITE_ANNUAL = "{elite_annual.id}"
STRIPE_PRICE_CREDITS_1000 = "{credits_1000.id}"
STRIPE_PRICE_CREDITS_5000 = "{credits_5000.id}"
STRIPE_PRICE_CREDITS_10000 = "{credits_10000.id}"
    """)
    
    print("\n🔗 View your products at: https://dashboard.stripe.com/test/products")

if __name__ == "__main__":
    try:
        create_products()
    except stripe.error.AuthenticationError:
        print("❌ Authentication Error!")
        print("Please set your Stripe API key at the top of this file")
        print("Get your test key from: https://dashboard.stripe.com/test/apikeys")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")