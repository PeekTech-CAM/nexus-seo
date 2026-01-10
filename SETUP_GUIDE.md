# Nexus SEO Intelligence - Complete Setup Guide

This guide will walk you through setting up your Nexus SEO Intelligence application with Supabase and Stripe.

## 📋 Prerequisites

- Python 3.8 or higher
- Stripe account (with live keys)
- Supabase account
- Git (optional)

## 🚀 Step 1: Project Setup

### 1.1 Create Project Directory

```bash
mkdir nexus-seo-intelligence
cd nexus-seo-intelligence
```

### 1.2 Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 1.3 Install Dependencies

Create `requirements.txt` with the provided content, then:

```bash
pip install -r requirements.txt
```

## 🗄️ Step 2: Supabase Setup

### 2.1 Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click "New Project"
3. Choose organization and name your project
4. Set a strong database password
5. Choose your region
6. Click "Create new project"

### 2.2 Create Database Tables

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste the entire content from `supabase_schema.sql`
4. Click "Run" to execute the SQL

This will create:
- `users` table
- `subscriptions` table
- `scans` table
- `webhook_events` table
- All necessary indexes and triggers

### 2.3 Get Supabase Credentials

1. Go to **Project Settings** → **API**
2. Copy these values:
   - **Project URL** (your `SUPABASE_URL`)
   - **anon public** key (your `SUPABASE_KEY`)
   - **service_role** key (your `SUPABASE_SERVICE_ROLE_KEY`)

## 💳 Step 3: Stripe Setup

### 3.1 Create Products and Prices

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Navigate to **Products** → **Add Product**

Create three products:

#### Product 1: Pro Plan
- Name: "Pro Plan"
- Description: "100 scans/month, basic reports"
- Pricing: 
  - Monthly: $29/month (Recurring)
  - Yearly: $290/year (Recurring)
- Copy the **Price ID** for each (starts with `price_`)

#### Product 2: Agency Plan
- Name: "Agency Plan"
- Description: "500 scans/month, advanced reports"
- Pricing:
  - Monthly: $79/month (Recurring)
  - Yearly: $790/year (Recurring)
- Copy the **Price ID** for each

#### Product 3: Elite Plan
- Name: "Elite Plan"
- Description: "Unlimited scans, white-label"
- Pricing:
  - Monthly: $199/month (Recurring)
- Copy the **Price ID**

### 3.2 Create Payment Links (Optional)

For the Pro plan, you can create direct payment links:

1. Go to **Payment Links** → **New**
2. Select your Pro product
3. Configure settings
4. Copy the payment link URL

### 3.3 Configure Webhooks

#### For Local Development:

1. Install Stripe CLI:
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Windows (using Scoop)
scoop install stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.17.0/stripe_1.17.0_linux_x86_64.tar.gz
tar -xvf stripe_1.17.0_linux_x86_64.tar.gz
```

2. Login to Stripe CLI:
```bash
stripe login
```

3. Forward webhooks to your local server:
```bash
stripe listen --forward-to localhost:8000/webhook
```

4. Copy the webhook signing secret (starts with `whsec_`)

#### For Production:

1. Go to **Developers** → **Webhooks** → **Add endpoint**
2. Endpoint URL: `https://your-domain.com/webhook`
3. Select events to listen for:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
4. Copy the **Signing secret**

## ⚙️ Step 4: Environment Configuration

### 4.1 Create .env File

Create a `.env` file in your project root with your actual credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://yehakxccvnmugkqhtmtj.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Stripe Configuration (LIVE MODE)
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Stripe Product IDs
STRIPE_PRICE_PRO_MONTHLY=price_xxxxx
STRIPE_PRICE_PRO_YEARLY=price_xxxxx
STRIPE_PRICE_AGENCY_MONTHLY=price_xxxxx
STRIPE_PRICE_AGENCY_YEARLY=price_xxxxx
STRIPE_PRICE_ELITE_MONTHLY=price_xxxxx

# Stripe Payment Links (Optional)
MONTHLY_PAYMENT_LINK=https://buy.stripe.com/xxxxx
YEARLY_PAYMENT_LINK=https://buy.stripe.com/xxxxx

# Application Settings
ENVIRONMENT=development
APP_BASE_URL=http://localhost:8501
APP_SECRET_KEY=change-this-in-production

# Flask Webhook Server
FLASK_SECRET_KEY=your-random-secret-key-here
PORT=8000

# Google AI (Optional - for future features)
GOOGLE_API_KEY=your_google_api_key
GEMINI_KEY=your_gemini_key

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@nexus-seo.com
```

### 4.2 Verify Configuration

Make sure all these variables are set correctly before proceeding.

## 🏃 Step 5: Running the Application

### 5.1 Start the Webhook Server (Terminal 1)

```bash
python webhook_server.py
```

You should see:
```
* Running on http://0.0.0.0:8000
```

### 5.2 Start Stripe CLI (Terminal 2) - For Local Dev

```bash
stripe listen --forward-to localhost:8000/webhook
```

You should see:
```
Ready! Your webhook signing secret is whsec_xxxxx (^C to quit)
```

### 5.3 Start Streamlit App (Terminal 3)

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## ✅ Step 6: Testing

### 6.1 Test User Registration

1. Open `http://localhost:8501`
2. Click "Don't have an account? Register here"
3. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
4. Click "Register"
5. Login with the credentials

### 6.2 Test Subscription Flow

1. Navigate to "Billing" in the sidebar
2. Click "Subscribe to Agency Monthly"
3. Use Stripe test card: `4242 4242 4242 4242`
4. Expiry: Any future date
5. CVC: Any 3 digits
6. Complete checkout

### 6.3 Verify Subscription

1. Check the webhook server logs - you should see events processed
2. In Streamlit, refresh and check "Billing" page
3. Your subscription should now show as active

### 6.4 Test SEO Scanning

1. Navigate to "New Scan"
2. Enter a URL: `https://example.com`
3. Click "Start Scan"
4. Wait for results

### 6.5 Test Report Generation

1. Navigate to "Scan Results"
2. Find your scan
3. Click "Generate Report"
4. Click "Download PDF"

## 🔍 Step 7: Verify Database

### 7.1 Check Supabase Tables

1. Go to Supabase Dashboard → **Table Editor**
2. Check `users` table - should have your test user
3. Check `subscriptions` table - should have active subscription
4. Check `scans` table - should have your scan results
5. Check `webhook_events` table - should have webhook logs

## 🐛 Troubleshooting

### Problem: Webhook events not being received

**Solution:**
- Ensure webhook server is running on port 8000
- Check Stripe CLI is forwarding to correct URL
- Verify webhook secret in `.env` matches Stripe CLI output

### Problem: Database connection errors

**Solution:**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check Supabase project is active
- Ensure tables were created successfully

### Problem: Stripe checkout not working

**Solution:**
- Verify `STRIPE_SECRET_KEY` is correct
- Check price IDs match your Stripe products
- Ensure you're in the correct mode (test/live)

### Problem: Authentication not working

**Solution:**
- Check Supabase RLS policies are set correctly
- Verify user table has correct structure
- Check password hashing is working

## 📊 Monitoring

### Check Application Logs

**Streamlit:**
- Logs appear in the terminal where you ran `streamlit run app.py`

**Webhook Server:**
- Logs appear in the terminal where you ran `python webhook_server.py`

**Supabase:**
- Go to **Logs** in Supabase dashboard to see database queries

**Stripe:**
- Go to **Developers** → **Webhooks** to see webhook delivery attempts
- Go to **Events** to see all Stripe events

## 🚀 Deployment (Production)

### Deploy to Cloud

For production deployment, consider:

1. **Streamlit Cloud** (for the main app)
2. **Heroku/Railway/Render** (for webhook server)
3. Update webhook URL in Stripe to your production domain
4. Change `ENVIRONMENT=production` in `.env`
5. Use production Stripe keys
6. Enable HTTPS

### Security Checklist

- [ ] Change all default secret keys
- [ ] Use environment variables (never commit `.env`)
- [ ] Enable Supabase RLS policies
- [ ] Use Stripe live mode keys
- [ ] Enable HTTPS for webhook endpoint
- [ ] Set up monitoring and alerting
- [ ] Regular database backups
- [ ] Rate limiting on API endpoints

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Supabase Documentation](https://supabase.com/docs)
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review application logs
3. Check Supabase and Stripe dashboards
4. Open an issue on GitHub

## ✨ Next Steps

Once everything is working:

1. Customize the branding
2. Add more SEO analysis features
3. Implement email notifications
4. Add analytics dashboard
5. Create API endpoints
6. Implement team features
7. Add white-label options

Good luck with your Nexus SEO Intelligence platform! 🚀