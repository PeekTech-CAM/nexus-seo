# Quick Reference - Your Nexus SEO Setup

This is a quick reference for YOUR specific configuration with your actual keys.

## 📋 Your Current Configuration

### Supabase
- **URL:** `https://yehakxccvnmugkqhtmtj.supabase.co`
- **Keys:** Already configured ✅

### Stripe (LIVE MODE)
- **Mode:** Production/Live
- **Keys:** Already configured ✅
- **Products:** Need to verify Price IDs

### Your Current Product IDs
Based on your .env, you have:
```
STRIPE_PRICE_PRO_MONTHLY=prod_Tj0yQ6xYTXxhZp
STRIPE_PRICE_PRO_YEARLY=prod_Tj0zimxF8Xr3dp
STRIPE_PRICE_AGENCY_MONTHLY=prod_Tj0zyPMhOwb79n
STRIPE_PRICE_AGENCY_YEARLY=prod_Tj10c8THfGfIvU
STRIPE_PRICE_ELITE_MONTHLY=prod_Tj10RWy0FVbqLA
```

⚠️ **IMPORTANT:** These look like Product IDs (prod_), NOT Price IDs (price_)

## ⚡ What You Need to Do

### Step 1: Get Correct Stripe Price IDs

1. Go to: https://dashboard.stripe.com/products
2. Click on each product (Pro, Agency, Elite)
3. Look for the **Price ID** (starts with `price_`, not `prod_`)
4. Copy each Price ID

Example of what you're looking for:
```
✅ CORRECT: price_1234567890abcdef
❌ WRONG:   prod_1234567890abcdef
```

### Step 2: Update Your .env File

Replace the product IDs with price IDs:

```env
# Change from prod_ to price_
STRIPE_PRICE_PRO_MONTHLY=price_YOUR_ACTUAL_PRICE_ID_HERE
STRIPE_PRICE_PRO_YEARLY=price_YOUR_ACTUAL_PRICE_ID_HERE
STRIPE_PRICE_AGENCY_MONTHLY=price_YOUR_ACTUAL_PRICE_ID_HERE
STRIPE_PRICE_AGENCY_YEARLY=price_YOUR_ACTUAL_PRICE_ID_HERE
STRIPE_PRICE_ELITE_MONTHLY=price_YOUR_ACTUAL_PRICE_ID_HERE
```

### Step 3: Set Up Supabase Database

1. Go to: https://supabase.com/dashboard/project/yehakxccvnmugkqhtmtj
2. Click **SQL Editor**
3. Click **New Query**
4. Copy ALL content from `supabase_schema.sql`
5. Paste and click **Run**

This creates your database tables.

### Step 4: Verify Webhook Secret

Your current webhook secret: `whsec_34edfdf1441d0af35228e2a64eb9******`

For local testing:
```bash
stripe listen --forward-to localhost:8000/webhook
```

This will give you a NEW webhook secret for local development. Update `.env` with it.

## 🚀 Running Your App

### Option 1: Easy Start (Recommended)

**On Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**On Windows:**
```bash
start.bat
```

### Option 2: Manual Start

**Terminal 1 - Webhook Server:**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
python webhook_server.py
```

**Terminal 2 - Streamlit:**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run app.py
```

**Terminal 3 - Stripe Webhooks:**
```bash
stripe listen --forward-to localhost:8000/webhook
```

## ✅ Testing Checklist

### 1. Test Registration
- [ ] Go to http://localhost:8501
- [ ] Register new user
- [ ] Login with credentials

### 2. Test Subscription
- [ ] Go to "Billing"
- [ ] Click subscribe
- [ ] Use test card: `4242 4242 4242 4242`
- [ ] Complete checkout
- [ ] Check subscription shows as active

### 3. Test SEO Scan
- [ ] Go to "New Scan"
- [ ] Enter URL: `https://example.com`
- [ ] Wait for results
- [ ] Check score appears

### 4. Test Reports
- [ ] Go to "Scan Results"
- [ ] Click "Generate Report"
- [ ] Click "Download PDF"

## 🔍 Verification Points

### Check Supabase Tables

Go to: https://supabase.com/dashboard/project/yehakxccvnmugkqhtmtj/editor

You should see these tables:
- [ ] `users` - Contains registered users
- [ ] `subscriptions` - Contains active subscriptions
- [ ] `scans` - Contains SEO scan results
- [ ] `webhook_events` - Contains webhook logs

### Check Stripe Dashboard

Go to: https://dashboard.stripe.com

- [ ] Products are created
- [ ] Prices are set
- [ ] Webhook endpoint is configured
- [ ] Test payment went through

## 🐛 If Something Breaks

### Can't connect to Supabase?
```bash
# Test connection
python -c "from supabase import create_client; print('OK')"
```

### Can't connect to Stripe?
```bash
# Test connection
python -c "import stripe; stripe.api_key='sk_test_...'; print(stripe.Product.list())"
```

### Webhooks not working?
- Check webhook server is running on port 8000
- Check Stripe CLI is forwarding
- Check webhook secret matches

### Database errors?
- Run `supabase_schema.sql` again
- Check all tables exist
- Verify service role key is set

## 📝 Important Files

Your complete file structure should be:

```
nexus-seo-intelligence/
├── .env                 ← Your credentials (NEVER commit this!)
├── .gitignore          ← Includes .env
├── app.py              ← Main Streamlit app
├── webhook_server.py   ← Stripe webhook handler
├── requirements.txt    ← Python packages
├── supabase_schema.sql ← Database schema
├── start.sh           ← Unix start script
├── start.bat          ← Windows start script
├── README.md          ← Documentation
├── SETUP_GUIDE.md     ← Detailed setup
└── services/
    ├── __init__.py
    ├── seo_scanner.py
    ├── report_generator.py
    ├── pdf_generator.py
    ├── email_service.py
    └── stripe_webhook_handler.py
```

## 💡 Pro Tips

1. **Always use 3 terminals** when developing:
   - Terminal 1: Webhook server
   - Terminal 2: Streamlit app
   - Terminal 3: Stripe CLI

2. **Check logs** when debugging:
   - Streamlit: Shows in terminal 2
   - Webhooks: Shows in terminal 1
   - Stripe: Dashboard → Events

3. **Use Debug page** in the app:
   - Go to "Debug Stripe" in sidebar
   - Click "Test Stripe Connection"
   - Click "Test Supabase Connection"

4. **Monitor everything**:
   - Supabase: Check logs panel
   - Stripe: Check events tab
   - Webhook events: Check `webhook_events` table

## 🎯 Next Steps After Setup

Once everything works:

1. **Customize branding** - Change colors, logo, text
2. **Add more SEO checks** - Extend scanner capabilities
3. **Set up email** - Configure SMTP for reports
4. **Deploy to production** - Use Streamlit Cloud + Railway
5. **Enable monitoring** - Set up alerts

## 📞 Need Help?

If you're stuck:

1. Check SETUP_GUIDE.md for detailed instructions
2. Review application logs
3. Check Supabase and Stripe dashboards
4. Look at webhook_events table for errors

---

**You're almost there! Just need to:**
1. ✅ Get correct Price IDs from Stripe
2. ✅ Run supabase_schema.sql
3. ✅ Start the apps
4. ✅ Test everything

Good luck! 🚀