-- ============================================================================
-- NEXUS SEO INTELLIGENCE - PRODUCTION DATABASE SCHEMA
-- ============================================================================
-- Database: PostgreSQL 14+ (Supabase)
-- Features: RLS, Triggers, Indexes, Audit Trail
-- ============================================================================
-- IMPORTANT: Copy ONLY from here down (including CREATE EXTENSION)
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

CREATE TYPE user_tier AS ENUM ('demo', 'pro', 'agency', 'elite');
CREATE TYPE subscription_status AS ENUM ('active', 'canceled', 'past_due', 'incomplete', 'trialing');
CREATE TYPE scan_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE issue_severity AS ENUM ('critical', 'high', 'medium', 'low', 'info');
CREATE TYPE transaction_type AS ENUM ('credit_purchase', 'credit_usage', 'credit_refund', 'credit_bonus', 'subscription_credit');

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- USERS (extends Supabase auth.users)
-- ----------------------------------------------------------------------------
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    company_name TEXT,
    avatar_url TEXT,
    
    -- Tier Management
    tier user_tier NOT NULL DEFAULT 'demo',
    tier_updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Credits
    credits_balance INTEGER NOT NULL DEFAULT 0,
    total_credits_purchased INTEGER NOT NULL DEFAULT 0,
    total_credits_used INTEGER NOT NULL DEFAULT 0,
    
    -- Usage Limits (per tier)
    monthly_scan_limit INTEGER NOT NULL DEFAULT 2,
    monthly_scans_used INTEGER NOT NULL DEFAULT 0,
    scan_limit_reset_date TIMESTAMPTZ DEFAULT NOW() + INTERVAL '1 month',
    
    -- Billing
    stripe_customer_id TEXT UNIQUE,
    stripe_subscription_id TEXT,
    
    -- Flags
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_admin BOOLEAN NOT NULL DEFAULT false,
    email_verified BOOLEAN NOT NULL DEFAULT false,
    onboarding_completed BOOLEAN NOT NULL DEFAULT false,
    
    -- Metadata
    signup_source TEXT,
    referral_code TEXT,
    utm_params JSONB,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ,
    
    -- Soft delete
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT positive_credits CHECK (credits_balance >= 0)
);

-- ----------------------------------------------------------------------------
-- SUBSCRIPTIONS
-- ----------------------------------------------------------------------------
CREATE TABLE public.subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    -- Stripe Data
    stripe_subscription_id TEXT NOT NULL UNIQUE,
    stripe_customer_id TEXT NOT NULL,
    stripe_price_id TEXT NOT NULL,
    stripe_product_id TEXT,
    
    -- Subscription Details
    status subscription_status NOT NULL DEFAULT 'incomplete',
    tier user_tier NOT NULL,
    
    -- Pricing
    currency TEXT NOT NULL DEFAULT 'usd',
    amount INTEGER NOT NULL, -- in cents
    interval TEXT NOT NULL, -- 'month' or 'year'
    
    -- Billing Periods
    current_period_start TIMESTAMPTZ NOT NULL,
    current_period_end TIMESTAMPTZ NOT NULL,
    trial_start TIMESTAMPTZ,
    trial_end TIMESTAMPTZ,
    
    -- Cancellation
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT false,
    canceled_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT positive_amount CHECK (amount > 0)
);

-- ----------------------------------------------------------------------------
-- SCANS (SEO Analysis Records)
-- ----------------------------------------------------------------------------
CREATE TABLE public.scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    -- Scan Target
    url TEXT NOT NULL,
    domain TEXT NOT NULL,
    
    -- Scan Execution
    status scan_status NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    
    -- SEO Scores (0-100)
    overall_score INTEGER,
    technical_score INTEGER,
    content_score INTEGER,
    performance_score INTEGER,
    accessibility_score INTEGER,
    
    -- Page Metadata
    title TEXT,
    meta_description TEXT,
    h1_tags TEXT[],
    word_count INTEGER,
    image_count INTEGER,
    link_count INTEGER,
    
    -- Technical Details
    page_size_kb INTEGER,
    load_time_ms INTEGER,
    http_status INTEGER,
    is_mobile_friendly BOOLEAN,
    has_ssl BOOLEAN,
    
    -- Issues Found
    critical_issues INTEGER DEFAULT 0,
    high_issues INTEGER DEFAULT 0,
    medium_issues INTEGER DEFAULT 0,
    low_issues INTEGER DEFAULT 0,
    
    -- Raw Data (for detailed analysis)
    raw_html TEXT, -- Store temporarily
    structured_data JSONB,
    issues_detail JSONB,
    
    -- AI Analysis Flag
    ai_analysis_requested BOOLEAN DEFAULT false,
    ai_analysis_completed BOOLEAN DEFAULT false,
    
    -- Error Handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Soft delete
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT valid_url CHECK (url ~* '^https?://'),
    CONSTRAINT valid_scores CHECK (
        overall_score BETWEEN 0 AND 100 OR overall_score IS NULL
    )
);

-- Index for user's recent scans
CREATE INDEX idx_scans_user_created ON public.scans(user_id, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_scans_domain ON public.scans(domain, created_at DESC);
CREATE INDEX idx_scans_status ON public.scans(status) WHERE status IN ('pending', 'processing');

-- ----------------------------------------------------------------------------
-- AI USAGE TRACKING
-- ----------------------------------------------------------------------------
CREATE TABLE public.ai_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    scan_id UUID REFERENCES public.scans(id) ON DELETE SET NULL,
    
    -- AI Request Details
    operation_type TEXT NOT NULL, -- 'audit', 'keyword_research', 'content_gap', 'roadmap'
    model_name TEXT NOT NULL, -- 'gemini-1.5-pro'
    
    -- Token Usage
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    
    -- Cost Calculation
    credits_consumed INTEGER NOT NULL,
    estimated_cost_usd DECIMAL(10, 6),
    
    -- Response Details
    response_time_ms INTEGER,
    cache_hit BOOLEAN DEFAULT false,
    
    -- Request/Response Storage
    prompt_template TEXT,
    prompt_variables JSONB,
    response_text TEXT,
    response_structured JSONB,
    
    -- Status
    success BOOLEAN NOT NULL DEFAULT true,
    error_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT positive_tokens CHECK (total_tokens > 0),
    CONSTRAINT positive_credits CHECK (credits_consumed >= 0)
);

CREATE INDEX idx_ai_usage_user_created ON public.ai_usage(user_id, created_at DESC);
CREATE INDEX idx_ai_usage_operation ON public.ai_usage(operation_type, created_at DESC);

-- ----------------------------------------------------------------------------
-- CREDIT TRANSACTIONS
-- ----------------------------------------------------------------------------
CREATE TABLE public.credit_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    -- Transaction Details
    type transaction_type NOT NULL,
    amount INTEGER NOT NULL, -- positive for additions, negative for usage
    balance_after INTEGER NOT NULL,
    
    -- Reference
    reference_id UUID, -- scan_id, subscription_id, or payment_intent_id
    reference_type TEXT, -- 'scan', 'subscription', 'purchase', 'adjustment'
    
    -- Description
    description TEXT NOT NULL,
    
    -- Admin Actions
    admin_id UUID REFERENCES public.profiles(id),
    admin_note TEXT,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT valid_balance CHECK (balance_after >= 0)
);

CREATE INDEX idx_credit_transactions_user ON public.credit_transactions(user_id, created_at DESC);
CREATE INDEX idx_credit_transactions_reference ON public.credit_transactions(reference_id);

-- ----------------------------------------------------------------------------
-- STRIPE EVENTS (Webhook Idempotency)
-- ----------------------------------------------------------------------------
CREATE TABLE public.stripe_events (
    id TEXT PRIMARY KEY, -- Stripe event ID
    type TEXT NOT NULL,
    
    -- Processing Status
    processed BOOLEAN NOT NULL DEFAULT false,
    processed_at TIMESTAMPTZ,
    
    -- Event Data
    data JSONB NOT NULL,
    
    -- Error Handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT max_retries CHECK (retry_count <= 5)
);

CREATE INDEX idx_stripe_events_processed ON public.stripe_events(processed, created_at);
CREATE INDEX idx_stripe_events_type ON public.stripe_events(type);

-- ----------------------------------------------------------------------------
-- AUDIT LOGS
-- ----------------------------------------------------------------------------
CREATE TABLE public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Actor
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    actor_email TEXT,
    
    -- Action
    action TEXT NOT NULL, -- 'scan_created', 'subscription_updated', 'credit_adjusted'
    resource_type TEXT NOT NULL, -- 'scan', 'subscription', 'user'
    resource_id UUID,
    
    -- Details
    changes JSONB, -- before/after values
    metadata JSONB DEFAULT '{}',
    
    -- Request Context
    ip_address INET,
    user_agent TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user ON public.audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_logs_resource ON public.audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_action ON public.audit_logs(action, created_at DESC);

-- ----------------------------------------------------------------------------
-- SEO RECOMMENDATIONS (AI Generated)
-- ----------------------------------------------------------------------------
CREATE TABLE public.seo_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_id UUID NOT NULL REFERENCES public.scans(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    -- Recommendation Details
    category TEXT NOT NULL, -- 'technical', 'content', 'keywords', 'performance'
    priority issue_severity NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    
    -- Implementation
    implementation_effort TEXT, -- 'low', 'medium', 'high'
    expected_impact TEXT, -- 'low', 'medium', 'high'
    estimated_time_hours INTEGER,
    
    -- Instructions
    action_steps TEXT[],
    code_examples TEXT,
    resources JSONB, -- links to documentation
    
    -- Tracking
    status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'dismissed'
    completed_at TIMESTAMPTZ,
    user_notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recommendations_scan ON public.seo_recommendations(scan_id);
CREATE INDEX idx_recommendations_user_status ON public.seo_recommendations(user_id, status);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.credit_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.stripe_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.seo_recommendations ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- PROFILES Policies
-- ----------------------------------------------------------------------------
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Admins can view all profiles"
    ON public.profiles FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE id = auth.uid() AND is_admin = true
        )
    );

-- ----------------------------------------------------------------------------
-- SUBSCRIPTIONS Policies
-- ----------------------------------------------------------------------------
CREATE POLICY "Users can view own subscriptions"
    ON public.subscriptions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all subscriptions"
    ON public.subscriptions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE id = auth.uid() AND is_admin = true
        )
    );

-- Service role can insert/update (for webhooks)
CREATE POLICY "Service can manage subscriptions"
    ON public.subscriptions FOR ALL
    USING (auth.jwt()->>'role' = 'service_role');

-- ----------------------------------------------------------------------------
-- SCANS Policies
-- ----------------------------------------------------------------------------
CREATE POLICY "Users can view own scans"
    ON public.scans FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own scans"
    ON public.scans FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own scans"
    ON public.scans FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all scans"
    ON public.scans FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE id = auth.uid() AND is_admin = true
        )
    );

-- ----------------------------------------------------------------------------
-- AI USAGE Policies
-- ----------------------------------------------------------------------------
CREATE POLICY "Users can view own AI usage"
    ON public.ai_usage FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all AI usage"
    ON public.ai_usage FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE id = auth.uid() AND is_admin = true
        )
    );

-- ----------------------------------------------------------------------------
-- CREDIT TRANSACTIONS Policies
-- ----------------------------------------------------------------------------
CREATE POLICY "Users can view own credit transactions"
    ON public.credit_transactions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all transactions"
    ON public.credit_transactions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE id = auth.uid() AND is_admin = true
        )
    );

-- ----------------------------------------------------------------------------
-- AUDIT LOGS Policies (Admin only)
-- ----------------------------------------------------------------------------
CREATE POLICY "Admins can view audit logs"
    ON public.audit_logs FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE id = auth.uid() AND is_admin = true
        )
    );

-- ----------------------------------------------------------------------------
-- RECOMMENDATIONS Policies
-- ----------------------------------------------------------------------------
CREATE POLICY "Users can view own recommendations"
    ON public.seo_recommendations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update own recommendations"
    ON public.seo_recommendations FOR UPDATE
    USING (auth.uid() = user_id);

-- ============================================================================
-- TRIGGERS & FUNCTIONS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Auto-update updated_at timestamp
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON public.subscriptions
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_scans_updated_at
    BEFORE UPDATE ON public.scans
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_recommendations_updated_at
    BEFORE UPDATE ON public.seo_recommendations
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ----------------------------------------------------------------------------
-- Auto-create profile on user signup
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, email_verified)
    VALUES (NEW.id, NEW.email, NEW.email_confirmed_at IS NOT NULL);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ----------------------------------------------------------------------------
-- Reset monthly scan limits
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.reset_monthly_scan_limits()
RETURNS void AS $$
BEGIN
    UPDATE public.profiles
    SET 
        monthly_scans_used = 0,
        scan_limit_reset_date = NOW() + INTERVAL '1 month'
    WHERE 
        scan_limit_reset_date <= NOW()
        AND is_active = true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Schedule this function to run daily via pg_cron or external scheduler

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Profiles
CREATE INDEX idx_profiles_email ON public.profiles(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_profiles_stripe_customer ON public.profiles(stripe_customer_id) WHERE stripe_customer_id IS NOT NULL;
CREATE INDEX idx_profiles_tier ON public.profiles(tier) WHERE is_active = true;

-- Subscriptions
CREATE INDEX idx_subscriptions_user ON public.subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_sub ON public.subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_status ON public.subscriptions(status, current_period_end);

-- ============================================================================
-- DATA RETENTION POLICIES
-- ============================================================================

-- Function to clean up old deleted records
CREATE OR REPLACE FUNCTION public.cleanup_soft_deleted_records()
RETURNS void AS $$
BEGIN
    -- Delete profiles soft-deleted > 90 days ago
    DELETE FROM public.profiles
    WHERE deleted_at < NOW() - INTERVAL '90 days';
    
    -- Delete scans > 1 year old (keep for analytics)
    -- Optionally archive to separate table first
    DELETE FROM public.scans
    WHERE created_at < NOW() - INTERVAL '1 year'
    AND deleted_at IS NOT NULL;
    
    -- Clean up processed Stripe events > 30 days
    DELETE FROM public.stripe_events
    WHERE processed = true
    AND created_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- ANALYTICS VIEWS (for admin dashboard)
-- ============================================================================

CREATE OR REPLACE VIEW public.v_revenue_metrics AS
SELECT 
    DATE_TRUNC('month', s.created_at) AS month,
    s.tier,
    COUNT(DISTINCT s.user_id) AS subscriber_count,
    SUM(s.amount) / 100.0 AS mrr_usd,
    SUM(s.amount) / 100.0 * 12 AS arr_usd
FROM public.subscriptions s
WHERE s.status = 'active'
GROUP BY 1, 2
ORDER BY 1 DESC, 2;

CREATE OR REPLACE VIEW public.v_user_metrics AS
SELECT 
    tier,
    COUNT(*) AS total_users,
    COUNT(*) FILTER (WHERE last_login_at > NOW() - INTERVAL '7 days') AS active_7d,
    COUNT(*) FILTER (WHERE last_login_at > NOW() - INTERVAL '30 days') AS active_30d,
    AVG(credits_balance) AS avg_credits,
    SUM(total_credits_used) AS total_credits_consumed
FROM public.profiles
WHERE is_active = true AND deleted_at IS NULL
GROUP BY tier;

-- ============================================================================
-- SAMPLE DATA (for development/testing)
-- ============================================================================

-- Insert admin user (update with real user ID after signup)
-- UPDATE public.profiles SET is_admin = true WHERE email = 'admin@nexusseo.com';

-- Grant necessary permissions for service operations
GRANT USAGE ON SCHEMA public TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;