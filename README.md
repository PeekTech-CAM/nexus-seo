# 🎯 NEXUS SEO INTELLIGENCE

**Enterprise-Grade AI-Powered SEO Analysis Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🚀 Overview

Nexus SEO Intelligence is a production-ready SaaS platform that combines advanced web scraping, technical SEO analysis, and Google Gemini PRO AI to deliver actionable insights for improving website search engine rankings.

### Key Features

✨ **Comprehensive SEO Scanning**
- Technical SEO analysis (HTTPS, mobile-friendly, page speed)
- On-page optimization (title, meta, headings, content)
- Content quality assessment (word count, structure)
- Accessibility checks (alt tags, semantic HTML)
- Structured data detection (JSON-LD, Schema.org)

🤖 **AI-Powered Insights**
- Gemini PRO-generated audit reports
- Keyword research & clustering
- Content gap analysis
- 30/60/90-day implementation roadmaps
- Competitive positioning recommendations

💳 **Monetization Ready**
- Stripe subscription management
- Credit-based AI usage system
- Multi-tier pricing (Demo, Pro, Agency, Elite)
- Automated billing with webhooks
- Customer portal for self-service

🔐 **Enterprise Security**
- Row Level Security (RLS) on all data
- Supabase authentication
- Webhook signature verification
- Rate limiting & DDoS protection
- Comprehensive audit logging

---

## 📋 Table of Contents

1. [Architecture](#architecture)
2. [Tech Stack](#tech-stack)
3. [Getting Started](#getting-started)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [API Documentation](#api-documentation)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│         Streamlit Multi-Page Application                     │
│  (Dashboard, Scanning, Analytics, AI Insights, Billing)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION SERVICES                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Auth Service │  │ SEO Scanner  │  │  AI Service  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Stripe Service│  │Credit Service│  │Report Service│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  DATA & EXTERNAL SERVICES                    │
│                                                              │
│  • Supabase (PostgreSQL + Auth)                             │
│  • Stripe (Payment Processing)                              │
│  • Google Gemini PRO (AI Analysis)                          │
│  • Flask Webhook Server (Event Processing)                  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: SEO Scan

```
User Input (URL) 
    → Validate & Check Limits 
    → Create Scan Record 
    → Fetch Page Content 
    → Parse HTML (BeautifulSoup) 
    → Extract Metadata & Analyze Technical/Content 
    → Calculate SEO Scores 
    → Store Results in Database 
    → [Optional] Trigger AI Analysis 
    → Display Results to User
```

### Data Flow: Stripe Payment

```
User Clicks Subscribe 
    → Create Stripe Checkout Session 
    → Redirect to Stripe 
    → User Completes Payment 
    → Stripe Webhook (checkout.session.completed) 
    → Verify Signature 
    → Check Idempotency 
    → Create Subscription Record 
    → Update User Tier 
    → Grant Credits 
    → Send Confirmation Email
```

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Python-based web framework
- **Custom CSS** - Modern, responsive UI inspired by Stripe/Linear
- **Charts** - Matplotlib, Plotly for visualizations

### Backend
- **Flask** - Webhook server for Stripe events
- **Gunicorn** - WSGI production server
- **Python 3.11+** - Core application language

### Database
- **Supabase** - Hosted PostgreSQL with Auth
- **Row Level Security (RLS)** - Database-level access control
- **PostgreSQL** - Relational database with advanced features

### AI & ML
- **Google Gemini PRO 1.5** - Advanced language model
- **Structured Prompts** - Engineered for consistent output quality

### Payment Processing
- **Stripe** - Subscriptions, one-time payments, customer portal
- **Webhooks** - Event-driven billing updates

### Infrastructure
- **Streamlit Cloud** / **AWS ECS** / **GCP Cloud Run** (deployment options)
- **Heroku** / **AWS Lambda** (webhook server options)
- **Cloudflare** - CDN and DDoS protection
- **Sentry** - Error monitoring

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ (for some dev tools)
- PostgreSQL 14+ or Supabase account
- Stripe account (test mode for development)
- Google Cloud account (for Gemini API)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nexus-seo-intelligence.git
cd nexus-seo-intelligence
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
# Import schema to Supabase via Dashboard or CLI
psql $DATABASE_URL < database/schema.sql
```

6. **Run migrations** (if any)
```bash
cd database/migrations
# Run migration scripts in order
```

### Running Locally

**Start Streamlit app:**
```bash
streamlit run app.py
```
Access at: http://localhost:8501

**Start webhook server (separate terminal):**
```bash
python webhook_server.py
```
Access at: http://localhost:8000

**Test webhooks locally with Stripe CLI:**
```bash
stripe listen --forward-to localhost:8000/webhooks/stripe
# Use webhook secret in .env
```

---

## ⚙️ Configuration

### Environment Variables

See `.env.example` for all required variables. Critical ones:

```bash
# Application
APP_BASE_URL=http://localhost:8501
ENVIRONMENT=development

# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Google AI
GOOGLE_API_KEY=your_gemini_api_key
```

### Stripe Setup

1. Create products in Stripe Dashboard:
   - Pro Monthly: $49/month
   - Pro Yearly: $470/year
   - Agency Monthly: $149/month
   - Agency Yearly: $1,430/year
   - Elite Monthly: $399/month

2. Copy price IDs to environment variables

3. Configure webhook endpoint:
   - URL: `https://your-domain.com/webhooks/stripe`
   - Events: `checkout.session.completed`, `customer.subscription.*`, `invoice.paid`, `invoice.payment_failed`

### Database Configuration

**Enable Row Level Security on all tables:**
```sql
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;
-- ... for all tables
```

**Create policies** (see schema.sql for complete policies)

---

## 🚢 Deployment

### Option 1: Streamlit Cloud (Quickest)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add environment variables in dashboard
5. Deploy

### Option 2: Docker + Cloud Run

```bash
# Build image
docker build -t nexusseo .

# Test locally
docker run -p 8501:8501 --env-file .env nexusseo

# Deploy to Cloud Run
gcloud run deploy nexusseo \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: AWS ECS

See `docs/DEPLOYMENT.md` for detailed AWS deployment guide.

### Webhook Server Deployment

**Heroku:**
```bash
heroku create nexusseo-webhooks
heroku config:set $(cat .env | xargs)
git push heroku main
```

**AWS Lambda:**
```python
# Use Mangum adapter
from webhook_server import app
from mangum import Mangum

handler = Mangum(app)
```

---

## 📚 API Documentation

### REST Endpoints

#### Create Scan
```http
POST /api/scans
Content-Type: application/json
Authorization: Bearer <token>

{
  "url": "https://example.com"
}

Response: 201 Created
{
  "scan_id": "uuid",
  "status": "pending"
}
```

#### Get Scan Results
```http
GET /api/scans/:scan_id
Authorization: Bearer <token>

Response: 200 OK
{
  "id": "uuid",
  "url": "https://example.com",
  "overall_score": 85,
  "technical_score": 90,
  "content_score": 80,
  ...
}
```

#### Create Checkout Session
```http
POST /api/billing/checkout
Content-Type: application/json
Authorization: Bearer <token>

{
  "tier": "pro",
  "interval": "monthly"
}

Response: 200 OK
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_..."
}
```

### Service Classes

#### SEOScanner
```python
from services.seo_scanner import SEOScanner

scanner = SEOScanner(supabase_client)
scan_id = scanner.scan_url(user_id, url)
```

#### AIService
```python
from services.ai_service import AIService

ai = AIService(supabase_client)
audit = ai.generate_seo_audit(user_id, scan_id, scan_data, user_tier)
```

#### StripeService
```python
from services.stripe_service import StripeService

stripe = StripeService(supabase_client)
checkout = stripe.create_checkout_session(user_id, email, tier, interval)
```

---

## 🧪 Testing

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=services --cov-report=html

# Specific test file
pytest tests/test_seo_scanner.py -v
```

### Test Structure
```
tests/
├── test_auth_service.py
├── test_seo_scanner.py
├── test_ai_service.py
├── test_stripe_integration.py
└── test_webhook_handling.py
```

### Example Test
```python
def test_seo_scanner_validates_url():
    scanner = SEOScanner(mock_supabase)
    
    # Valid URL
    assert scanner._normalize_url("example.com") == "https://example.com"
    
    # Invalid URL
    assert scanner._normalize_url("not-a-url") is None
```

### Integration Testing

**Test Stripe webhooks:**
```bash
stripe trigger checkout.session.completed
```

**Test AI generation:**
```python
pytest tests/test_ai_service.py::test_generate_audit -s
```

---

## 📊 Monitoring

### Error Tracking
```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    environment=os.getenv('ENVIRONMENT')
)
```

### Performance Monitoring
```python
@monitor_performance('seo_scan')
def perform_scan(url):
    # Automatically logged to monitoring service
    pass
```

### Health Checks
```bash
# Webhook server health
curl https://your-webhook-server.com/health

# Application health
curl https://your-app.com/api/health
```

---

## 🔒 Security

### Best Practices Implemented

✅ Row Level Security (RLS) on all database tables  
✅ Webhook signature verification  
✅ JWT authentication  
✅ Input validation & sanitization  
✅ Rate limiting  
✅ SQL injection prevention (parameterized queries)  
✅ XSS protection (HTML sanitization)  
✅ HTTPS enforcement  
✅ Secure environment variable handling  
✅ Audit logging for sensitive operations  

### Security Checklist

- [ ] Rotate API keys quarterly
- [ ] Review access logs monthly
- [ ] Update dependencies weekly
- [ ] Run security scans (Snyk, Dependabot)
- [ ] Perform penetration testing quarterly
- [ ] Review and update security policies

---

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style

**Format code with Black:**
```bash
black .
```

**Lint with Flake8:**
```bash
flake8 services/ pages/
```

**Type check with MyPy:**
```bash
mypy services/
```

### Commit Convention

```
feat: Add keyword clustering feature
fix: Resolve scan timeout issue
docs: Update API documentation
test: Add integration tests for billing
refactor: Simplify credit deduction logic
```

---

## 📈 Roadmap

### Q1 2025
- [ ] Multi-language support
- [ ] Advanced competitor analysis
- [ ] White-label reporting for agencies
- [ ] API access for Pro+ tiers
- [ ] Mobile app (React Native)

### Q2 2025
- [ ] WordPress plugin integration
- [ ] Shopify app
- [ ] Automated weekly reports
- [ ] Custom alerts & notifications
- [ ] Team collaboration features

### Q3 2025
- [ ] Machine learning ranking predictions
- [ ] Content generation assistant
- [ ] Video content optimization
- [ ] Local SEO features
- [ ] Agency dashboard

---

## 💬 Support

### Documentation
- [User Guide](https://docs.nexusseo.com)
- [API Reference](https://api.nexusseo.com/docs)
- [FAQ](https://nexusseo.com/faq)

### Contact
- **Email**: support@nexusseo.com
- **Slack**: [Join Community](https://slack.nexusseo.com)
- **Twitter**: [@NexusSEO](https://twitter.com/nexusseo)

### Reporting Issues
Please use GitHub Issues for bug reports and feature requests.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing framework
- **Supabase** - For the excellent backend-as-a-service
- **Stripe** - For reliable payment processing
- **Google** - For Gemini PRO AI capabilities
- **Community** - For feedback and contributions

---

## 📝 Changelog

### v1.0.0 (2025-01-03)
- Initial production release
- Core SEO scanning engine
- AI-powered analysis with Gemini PRO
- Stripe subscription management
- Multi-tier pricing system
- Comprehensive admin dashboard

---

**Built with ❤️ for the SEO community**

*Nexus SEO Intelligence - Where AI Meets Search Optimization*