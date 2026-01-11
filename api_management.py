"""
API Management - Manage Your API Access
Control API keys, monitor usage, and manage integrations
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import string

# Page config
st.set_page_config(page_title="API Management", page_icon="🔌", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .api-key-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-family: 'Courier New', monospace;
    }
    .code-block {
        background: #1a1a1a;
        color: #00ff00;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
    .endpoint-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = [
        {
            'id': 1,
            'name': 'Production Key',
            'key': 'sk_live_' + ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            'created': datetime(2025, 11, 1),
            'last_used': datetime.now() - timedelta(hours=2),
            'requests_today': 1234,
            'requests_month': 45678,
            'rate_limit': 10000,
            'status': 'Active',
            'scopes': ['read', 'write', 'admin']
        },
        {
            'id': 2,
            'name': 'Development Key',
            'key': 'sk_test_' + ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            'created': datetime(2025, 12, 15),
            'last_used': datetime.now() - timedelta(days=3),
            'requests_today': 45,
            'requests_month': 890,
            'rate_limit': 1000,
            'status': 'Active',
            'scopes': ['read']
        }
    ]

if 'api_logs' not in st.session_state:
    st.session_state.api_logs = []

# Helper function to generate API key
def generate_api_key():
    return 'sk_live_' + ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Header
st.markdown('<div class="main-header">🔌 API Management</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Manage your API keys, monitor usage, and integrate with external services</div>', unsafe_allow_html=True)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

total_requests_today = sum(k['requests_today'] for k in st.session_state.api_keys)
total_requests_month = sum(k['requests_month'] for k in st.session_state.api_keys)
active_keys = sum(1 for k in st.session_state.api_keys if k['status'] == 'Active')

with col1:
    st.metric("Active API Keys", active_keys)
with col2:
    st.metric("Requests Today", f"{total_requests_today:,}")
with col3:
    st.metric("Requests This Month", f"{total_requests_month:,}")
with col4:
    st.metric("Success Rate", "99.7%")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔑 API Keys", "📊 Usage", "📖 Documentation", "🔗 Integrations", "⚙️ Settings"])

with tab1:
    st.markdown("### 🔑 Your API Keys")
    
    # Add new key button
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("➕ Create New Key", use_container_width=True):
            st.session_state['show_create_key'] = True
    
    # Create key form
    if st.session_state.get('show_create_key', False):
        with st.form("create_key_form"):
            st.markdown("#### Create New API Key")
            
            key_name = st.text_input("Key Name*", placeholder="Production Key")
            
            col1, col2 = st.columns(2)
            
            with col1:
                key_type = st.selectbox("Key Type", options=['Live', 'Test'])
                rate_limit = st.number_input("Rate Limit (requests/day)", min_value=100, value=10000, step=100)
            
            with col2:
                scopes = st.multiselect(
                    "Permissions",
                    options=['read', 'write', 'delete', 'admin'],
                    default=['read', 'write']
                )
                expires = st.checkbox("Set expiration")
                
                if expires:
                    expiry_date = st.date_input("Expiry Date")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("Create Key", type="primary", use_container_width=True):
                    if key_name:
                        new_key = {
                            'id': max([k['id'] for k in st.session_state.api_keys]) + 1,
                            'name': key_name,
                            'key': generate_api_key() if key_type == 'Live' else 'sk_test_' + ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                            'created': datetime.now(),
                            'last_used': None,
                            'requests_today': 0,
                            'requests_month': 0,
                            'rate_limit': rate_limit,
                            'status': 'Active',
                            'scopes': scopes
                        }
                        
                        st.session_state.api_keys.append(new_key)
                        st.session_state['show_create_key'] = False
                        st.success(f"✅ API key '{key_name}' created!")
                        st.rerun()
                    else:
                        st.error("Please provide a key name")
            
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state['show_create_key'] = False
                    st.rerun()
    
    st.markdown("---")
    
    # Display existing keys
    for key in st.session_state.api_keys:
        with st.expander(f"**{key['name']}** - {key['status']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**API Key:**")
                
                # Show key with copy button
                key_display = key['key'] if st.session_state.get(f'show_key_{key["id"]}', False) else key['key'][:12] + '•' * 20
                
                st.markdown(f"""
                <div class="api-key-card">
                    {key_display}
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("👁️ Show/Hide", key=f"toggle_{key['id']}", use_container_width=True):
                        st.session_state[f'show_key_{key["id"]}'] = not st.session_state.get(f'show_key_{key["id"]}', False)
                        st.rerun()
                
                with col_b:
                    if st.button("📋 Copy", key=f"copy_{key['id']}", use_container_width=True):
                        st.success("Copied to clipboard!")
                
                with col_c:
                    if st.button("🔄 Regenerate", key=f"regen_{key['id']}", use_container_width=True):
                        key['key'] = generate_api_key()
                        st.success("Key regenerated!")
                        st.rerun()
            
            with col2:
                st.metric("Requests Today", f"{key['requests_today']:,}")
                st.metric("Requests This Month", f"{key['requests_month']:,}")
                st.metric("Rate Limit", f"{key['rate_limit']:,}/day")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Created:** {key['created'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Last Used:** {key['last_used'].strftime('%Y-%m-%d %H:%M') if key['last_used'] else 'Never'}")
            
            with col2:
                st.markdown(f"**Permissions:** {', '.join(key['scopes'])}")
                
                usage_percent = (key['requests_today'] / key['rate_limit']) * 100
                st.progress(usage_percent / 100)
                st.caption(f"Usage: {usage_percent:.1f}% of daily limit")
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if key['status'] == 'Active':
                    if st.button("⏸️ Disable", key=f"disable_{key['id']}", use_container_width=True):
                        key['status'] = 'Disabled'
                        st.success("Key disabled")
                        st.rerun()
                else:
                    if st.button("▶️ Enable", key=f"enable_{key['id']}", use_container_width=True):
                        key['status'] = 'Active'
                        st.success("Key enabled")
                        st.rerun()
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{key['id']}", use_container_width=True):
                    st.info("Edit mode coming soon")
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{key['id']}", use_container_width=True):
                    st.session_state.api_keys = [k for k in st.session_state.api_keys if k['id'] != key['id']]
                    st.success("Key deleted")
                    st.rerun()

with tab2:
    st.markdown("### 📊 API Usage Analytics")
    
    # Time range selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_range = st.selectbox(
            "Time Range",
            options=['Last 24 Hours', 'Last 7 Days', 'Last 30 Days', 'Last 90 Days']
        )
    
    with col2:
        if st.button("📥 Export Data", use_container_width=True):
            st.info("Exporting usage data...")
    
    # Usage chart
    st.markdown("#### 📈 Request Volume")
    
    import plotly.graph_objects as go
    
    if time_range == 'Last 24 Hours':
        hours = [f"{i:02d}:00" for i in range(24)]
        requests = [random.randint(50, 200) for _ in range(24)]
        x_data = hours
    else:
        days = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30, 0, -1)]
        requests = [random.randint(500, 2000) for _ in range(30)]
        x_data = days
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=requests,
        mode='lines+markers',
        name='Requests',
        fill='tozeroy',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Requests",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Endpoints breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Top Endpoints")
        
        endpoints_data = {
            'Endpoint': ['/api/scan', '/api/keywords', '/api/backlinks', '/api/rank', '/api/audit'],
            'Requests': [15234, 12456, 8923, 6234, 4567],
            'Avg Response': ['245ms', '189ms', '312ms', '156ms', '523ms']
        }
        
        st.dataframe(endpoints_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 🌍 Geographic Distribution")
        
        geo_data = {
            'Country': ['United States', 'United Kingdom', 'Germany', 'Canada', 'Australia'],
            'Requests': [25000, 8000, 6000, 5000, 3500],
            'Percentage': ['54%', '17%', '13%', '11%', '8%']
        }
        
        st.dataframe(geo_data, use_container_width=True, hide_index=True)
    
    # Response codes
    st.markdown("#### 📊 Response Codes")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("200 OK", "46,234", "+2.3%")
    with col2:
        st.metric("400 Bad Request", "234", "-15%")
    with col3:
        st.metric("401 Unauthorized", "45", "-30%")
    with col4:
        st.metric("500 Server Error", "12", "-50%")

with tab3:
    st.markdown("### 📖 API Documentation")
    
    # Quick start
    st.markdown("#### 🚀 Quick Start")
    
    st.markdown("""
    Get started with our API in minutes. Here's a basic example:
    """)
    
    st.markdown("""
    ```python
    import requests
    
    # Your API key
    api_key = "sk_live_your_key_here"
    
    # Make a request
    response = requests.get(
        "https://api.seotools.com/v1/scan",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"url": "https://example.com"}
    )
    
    # Process the response
    data = response.json()
    print(data)
    ```
    """)
    
    st.markdown("---")
    
    # Endpoints
    st.markdown("#### 🔌 Available Endpoints")
    
    endpoints = [
        {
            'method': 'GET',
            'endpoint': '/v1/scan',
            'description': 'Scan a website for SEO issues',
            'params': 'url (required), depth (optional)'
        },
        {
            'method': 'GET',
            'endpoint': '/v1/keywords',
            'description': 'Get keyword suggestions and data',
            'params': 'keyword (required), location (optional)'
        },
        {
            'method': 'GET',
            'endpoint': '/v1/backlinks',
            'description': 'Retrieve backlink profile',
            'params': 'domain (required), limit (optional)'
        },
        {
            'method': 'POST',
            'endpoint': '/v1/rank',
            'description': 'Check keyword rankings',
            'params': 'keyword (required), url (required), location (optional)'
        },
        {
            'method': 'GET',
            'endpoint': '/v1/audit',
            'description': 'Perform comprehensive site audit',
            'params': 'url (required), checks (optional)'
        }
    ]
    
    for endpoint in endpoints:
        method_color = '#10b981' if endpoint['method'] == 'GET' else '#3b82f6'
        
        st.markdown(f"""
        <div class="endpoint-card">
            <span style="background: {method_color}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: 600; margin-right: 0.5rem;">
                {endpoint['method']}
            </span>
            <code style="background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px;">
                {endpoint['endpoint']}
            </code>
            <p style="margin-top: 0.5rem; color: #666;">
                {endpoint['description']}
            </p>
            <p style="margin-top: 0.25rem; font-size: 0.875rem; color: #999;">
                Parameters: {endpoint['params']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Code examples
    st.markdown("#### 💻 Code Examples")
    
    language = st.selectbox(
        "Select language",
        options=['Python', 'JavaScript', 'cURL', 'PHP', 'Ruby']
    )
    
    if language == 'Python':
        st.code("""
import requests

api_key = "your_api_key"
url = "https://api.seotools.com/v1/scan"

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {api_key}"},
    params={"url": "https://example.com"}
)

print(response.json())
        """, language='python')
    
    elif language == 'JavaScript':
        st.code("""
const apiKey = "your_api_key";
const url = "https://api.seotools.com/v1/scan";

fetch(url + "?url=https://example.com", {
    headers: {
        "Authorization": `Bearer ${apiKey}`
    }
})
.then(response => response.json())
.then(data => console.log(data));
        """, language='javascript')
    
    elif language == 'cURL':
        st.code("""
curl -X GET "https://api.seotools.com/v1/scan?url=https://example.com" \\
  -H "Authorization: Bearer your_api_key"
        """, language='bash')

with tab4:
    st.markdown("### 🔗 Integrations")
    
    st.markdown("Connect your SEO tools with popular platforms and services.")
    
    # Available integrations
    integrations = [
        {
            'name': 'Google Analytics',
            'icon': '📊',
            'description': 'Sync SEO data with your GA4 property',
            'status': 'Available'
        },
        {
            'name': 'Google Search Console',
            'icon': '🔍',
            'description': 'Import search performance data automatically',
            'status': 'Available'
        },
        {
            'name': 'Slack',
            'icon': '💬',
            'description': 'Get notifications in your Slack workspace',
            'status': 'Available'
        },
        {
            'name': 'Zapier',
            'icon': '⚡',
            'description': 'Connect with 5000+ apps via Zapier',
            'status': 'Available'
        },
        {
            'name': 'WordPress',
            'icon': '📝',
            'description': 'Monitor and optimize your WordPress sites',
            'status': 'Available'
        },
        {
            'name': 'Shopify',
            'icon': '🛒',
            'description': 'Track SEO for your Shopify store',
            'status': 'Coming Soon'
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, integration in enumerate(integrations):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 1rem;">
                    <div style="font-size: 2rem;">{integration['icon']}</div>
                    <h4 style="margin: 0.5rem 0;">{integration['name']}</h4>
                    <p style="color: #666; font-size: 0.9rem;">{integration['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if integration['status'] == 'Available':
                    if st.button(f"Connect {integration['name']}", key=f"connect_{integration['name']}", use_container_width=True):
                        st.info(f"Opening {integration['name']} connection...")
                else:
                    st.button("Coming Soon", disabled=True, use_container_width=True)
    
    st.markdown("---")
    
    # Webhooks
    st.markdown("#### 🔔 Webhooks")
    
    st.markdown("Configure webhooks to receive real-time notifications.")
    
    webhook_url = st.text_input("Webhook URL", placeholder="https://your-domain.com/webhook")
    
    webhook_events = st.multiselect(
        "Events to subscribe",
        options=[
            'scan.completed',
            'scan.failed',
            'keyword.rank_changed',
            'backlink.new',
            'backlink.lost',
            'alert.triggered'
        ]
    )
    
    if st.button("Save Webhook", use_container_width=True):
        if webhook_url:
            st.success("✅ Webhook configured successfully!")
        else:
            st.error("Please provide a webhook URL")

with tab5:
    st.markdown("### ⚙️ API Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔒 Security")
        
        require_https = st.checkbox("Require HTTPS", value=True)
        ip_whitelist = st.checkbox("Enable IP whitelist", value=False)
        
        if ip_whitelist:
            st.text_area("Allowed IP addresses (one per line)", height=100)
        
        st.markdown("#### ⚡ Rate Limiting")
        
        default_rate_limit = st.number_input(
            "Default rate limit (requests/day)",
            min_value=100,
            value=10000,
            step=100
        )
        
        burst_limit = st.number_input(
            "Burst limit (requests/minute)",
            min_value=10,
            value=100,
            step=10
        )
        
        st.markdown("#### 🔔 Alerts")
        
        alert_on_limit = st.checkbox("Alert when approaching rate limit", value=True)
        alert_threshold = st.slider("Alert threshold (%)", min_value=50, max_value=100, value=80)
    
    with col2:
        st.markdown("#### 📊 Logging")
        
        log_requests = st.checkbox("Log all requests", value=True)
        log_responses = st.checkbox("Log response bodies", value=False)
        
        retention_period = st.selectbox(
            "Log retention period",
            options=['7 days', '30 days', '90 days', '1 year']
        )
        
        st.markdown("#### 🔄 Versioning")
        
        api_version = st.selectbox(
            "Default API version",
            options=['v1 (current)', 'v2 (beta)']
        )
        
        force_version = st.checkbox("Force specific version", value=False)
        
        st.markdown("#### 💾 Backups")
        
        auto_backup = st.checkbox("Auto-backup API configurations", value=True)
        
        if auto_backup:
            backup_frequency = st.selectbox(
                "Backup frequency",
                options=['Daily', 'Weekly', 'Monthly']
            )
    
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.success("✅ API settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("💡 **Need Help?** Check out our [API Documentation](https://docs.seotools.com) or contact support@seotools.com")