# Nexus SEO Intelligence 🔍

A comprehensive SEO analysis and monitoring platform with Stripe billing integration, built with Streamlit and Supabase.

![License](https://img.shields.io/badge/license-OFL--1.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

## ✨ Features

- 🔐 **Secure Authentication** - User registration and login with Supabase
- 🔍 **Comprehensive SEO Analysis** - Deep website auditing
- 📊 **Professional Reports** - Detailed SEO reports with scoring
- 💳 **Stripe Integration** - Multiple subscription tiers
- 📄 **PDF Export** - Download reports as professional PDFs
- 📧 **Email Notifications** - Automated report delivery (optional)
- 🎯 **Real-time Updates** - Live subscription status
- 🔗 **Webhook Processing** - Automatic payment handling
- 📈 **Scan History** - Track all your SEO audits

## 🎯 Subscription Plans

### 🥉 Pro Plan
- **$29/month** or **$290/year**
- 100 scans per month
- Basic SEO reports
- Email support
- PDF export

### 🥈 Agency Plan
- **$79/month** or **$790/year**
- 500 scans per month
- Advanced analytics
- Priority support
- API access
- Multi-user access

### 🥇 Elite Plan
- **$199/month**
- Unlimited scans
- White-label reports
- Dedicated support
- Custom integrations
- SLA guarantee

## 🏗️ Tech Stack

- **Frontend:** Streamlit
- **Database:** Supabase (PostgreSQL)
- **Payments:** Stripe
- **Backend:** Flask (webhook server)
- **Reports:** ReportLab (PDF generation)
- **Scraping:** BeautifulSoup4, Requests

## 📁 Project Structure

```
nexus-seo-intelligence/
├── app.py                          # Main Streamlit application
├── webhook_server.py               # Flask webhook handler
├── services/
│   ├── __init__.py
│   ├── seo_scanner.py             # SEO analysis engine
│   ├── report_generator.py        # Markdown report generation
│   ├── pdf_generator.py           # PDF report creation
│   ├── email_service.py           # Email notifications
│   └── stripe_webhook_handler.py  # Webhook event processing
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Example environment configuration
├── requirements.txt                # Python dependencies
├── supabase_schema.sql            # Database schema
├── SETUP_GUIDE.md                 # Detailed setup instructions
├── start.sh                        # Unix/Mac startup script
├── start.bat                       # Windows startup script
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Stripe account (live or test mode)
- Supabase account
- Git (optional)

### 1. Clone or Download

```bash
git clone https://github.com/yourusername/nexus-seo-intelligence.git
cd nexus-seo-intelligence
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file with your credentials:

```env
# Supabase
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Stripe
STRIPE_SECRET_KEY=sk_live_or_test_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Stripe Price IDs
STRIPE_PRICE_PRO_MONTHLY=price_xxxxx
STRIPE_PRICE_PRO_YEARLY=price_xxxxx
STRIPE_PRICE_AGENCY_MONTHLY=price_xxxxx
STRIPE_PRICE_AGENCY_YEARLY=price_xxxxx
STRIPE_PRICE_ELITE_MONTHLY=price_xxxxx

# Application
APP_BASE_URL=http://localhost:8501
PORT=8000
```

### 4. Set Up Database

1. Go to your Supabase project
2. Open SQL Editor
3. Run the contents of `supabase_schema.sql`

### 5. Start the Application

**Easy Way (Recommended):**

```bash
# On macOS/Linux
chmod +x start.sh
./start.sh

# On Windows
start.bat
```

**Manual Way:**

```bash
# Terminal 1: Start webhook server
python webhook_server.py

# Terminal 2: Start Streamlit (in another terminal)
streamlit run app.py

# Terminal 3: Forward Stripe webhooks (in another terminal)
stripe listen --forward-to localhost:8000/webhook
```

### 6. Access the Application

- **Main App:** http://localhost:8501
- **Webhook Server:** http://localhost:8000

## 📚 Detailed Setup

For complete setup instructions including Stripe configuration, webhook setup, and deployment, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## 🔧 Configuration

### Stripe Products Setup

You need to create products in Stripe Dashboard:

1. Go to Stripe Dashboard → Products
2. Create three products (Pro, Agency, Elite)
3. Add monthly and/or yearly pricing
4. Copy the Price IDs to your `.env` file

### Webhook Configuration

**Local Development:**

```bash
stripe listen --forward-to localhost:8000/webhook
```

**Production:**

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-domain.com/webhook`
3. Select these events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`

## 🧪 Testing

### Test User Flow

1. Register a new account
2. Login with credentials
3. Go to Billing page
4. Subscribe to a plan using Stripe test card:
   - Card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits

### Test SEO Scanner

1. Navigate to "New Scan"
2. Enter URL: `https://example.com`
3. Click "Start Scan"
4. View results

### Test Reports

1. Go to "Scan Results"
2. Click "Generate Report"
3. Click "Download PDF"

## 🔍 SEO Analysis Features

The scanner analyzes:

- ✅ Meta tags (title, description, OG tags)
- ✅ Heading structure (H1-H6)
- ✅ Image optimization (alt text, titles)
- ✅ Link analysis (internal/external)
- ✅ Content quality (word count, readability)
- ✅ Technical SEO (SSL, sitemap, robots.txt)
- ✅ Mobile optimization
- ✅ Page performance
- ✅ Structured data detection

## 📊 Reports Include

- Overall SEO score (0-100)
- Detailed analysis of each factor
- Prioritized recommendations
- Visual metrics and charts
- Exportable PDF format

## 🛠️ Development

### Project Architecture

```
┌─────────────────┐
│  Streamlit UI   │ ← User Interface
└────────┬────────┘
         │
    ┌────▼─────┐
    │   App    │ ← Main Application Logic
    └────┬─────┘
         │
    ┌────▼────────────────┐
    │   Services Layer    │
    ├─────────────────────┤
    │ • SEO Scanner       │
    │ • Report Generator  │
    │ • PDF Generator     │
    │ • Email Service     │
    └────┬────────────────┘
         │
    ┌────▼─────────────────┐
    │  External Services   │
    ├──────────────────────┤
    │ • Supabase (DB)      │
    │ • Stripe (Payments)  │
    │ • SMTP (Email)       │
    └──────────────────────┘
```

### Adding New Features

1. **New SEO Check:**
   - Add method to `services/seo_scanner.py`
   - Update scoring in `_calculate_score()`

2. **New Report Section:**
   - Add section to `services/report_generator.py`
   - Update PDF generator if needed

3. **New Subscription Tier:**
   - Create product in Stripe
   - Add price ID to `.env`
   - Update billing page in `app.py`

## 🐛 Troubleshooting

### Common Issues

**Problem:** Can't connect to Supabase
- Verify URL and keys in `.env`
- Check Supabase project status
- Ensure tables are created

**Problem:** Stripe webhooks not working
- Verify webhook secret matches
- Check webhook server is running
- Review Stripe dashboard events

**Problem:** SEO scan fails
- Check website is accessible
- Verify no firewall blocks
- Review error logs

**Problem:** Database errors
- Run `supabase_schema.sql` again
- Check RLS policies
- Verify service role key

For more troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## 🚀 Deployment

### Recommended Stack

- **Frontend:** Streamlit Cloud or Heroku
- **Webhook Server:** Railway, Render, or Heroku
- **Database:** Supabase (included)
- **Payments:** Stripe (included)

### Environment Variables

Set these in your deployment platform:

```
SUPABASE_URL
SUPABASE_KEY
SUPABASE_SERVICE_ROLE_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
STRIPE_PRICE_PRO_MONTHLY
STRIPE_PRICE_PRO_YEARLY
STRIPE_PRICE_AGENCY_MONTHLY
STRIPE_PRICE_AGENCY_YEARLY
STRIPE_PRICE_ELITE_MONTHLY
APP_BASE_URL
```

### Security Checklist

- [ ] Use production Stripe keys
- [ ] Enable HTTPS
- [ ] Set strong secret keys
- [ ] Enable Supabase RLS
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Enable database backups
- [ ] Use rate limiting

## 📈 Monitoring

### Application Logs

- Streamlit: Terminal output
- Webhook Server: Flask logs
- Database: Supabase logs panel

### Stripe Events

- Dashboard → Developers → Events
- Dashboard → Developers → Webhooks

### Database Metrics

- Supabase Dashboard → Logs
- Check `webhook_events` table

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the OFL-1.1 License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Database by [Supabase](https://supabase.com/)
- Payments by [Stripe](https://stripe.com/)
- PDF generation with [ReportLab](https://www.reportlab.com/)

## 📞 Support

- Documentation: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Issues: [GitHub Issues](https://github.com/yourusername/nexus-seo-intelligence/issues)
- Email: support@nexus-seo.com

## 🗺️ Roadmap

- [ ] API endpoints for third-party integration
- [ ] Scheduled scans and monitoring
- [ ] Email report delivery
- [ ] Team collaboration features
- [ ] Custom branding/white-label
- [ ] Advanced analytics dashboard
- [ ] Competitor analysis
- [ ] Keyword tracking
- [ ] Backlink monitoring
- [ ] Mobile app

---

**Made with ❤️ for the SEO community**

*Start optimizing your websites today!* 🚀