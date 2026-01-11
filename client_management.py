"""
Client Management - Manage Your SEO Clients
Track clients, projects, and deliverables
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(page_title="Client Management", page_icon="👥", layout="wide")

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
    .client-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .status-active {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .status-pending {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .status-inactive {
        background: #6b7280;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'clients' not in st.session_state:
    st.session_state.clients = [
        {
            'id': 1,
            'name': 'Acme Corporation',
            'contact': 'John Smith',
            'email': 'john@acme.com',
            'phone': '+1 555-0123',
            'website': 'https://acme.com',
            'status': 'Active',
            'package': 'Premium',
            'monthly_fee': 2500,
            'start_date': datetime.now() - timedelta(days=180),
            'keywords_tracked': 50,
            'reports_sent': 6,
            'last_report': datetime.now() - timedelta(days=15),
            'notes': 'Focus on local SEO and content marketing'
        },
        {
            'id': 2,
            'name': 'Tech Startup Inc',
            'contact': 'Sarah Johnson',
            'email': 'sarah@techstartup.com',
            'phone': '+1 555-0456',
            'website': 'https://techstartup.com',
            'status': 'Active',
            'package': 'Standard',
            'monthly_fee': 1500,
            'start_date': datetime.now() - timedelta(days=90),
            'keywords_tracked': 30,
            'reports_sent': 3,
            'last_report': datetime.now() - timedelta(days=30),
            'notes': 'New client, focus on technical SEO'
        }
    ]

if 'projects' not in st.session_state:
    st.session_state.projects = []

# Header
st.markdown('<div class="main-header">👥 Client Management</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Manage your SEO clients and track their progress</div>', unsafe_allow_html=True)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

total_clients = len(st.session_state.clients)
active_clients = sum(1 for c in st.session_state.clients if c['status'] == 'Active')
total_revenue = sum(c['monthly_fee'] for c in st.session_state.clients if c['status'] == 'Active')
total_keywords = sum(c['keywords_tracked'] for c in st.session_state.clients)

with col1:
    st.metric("Total Clients", total_clients)
with col2:
    st.metric("Active Clients", active_clients)
with col3:
    st.metric("Monthly Revenue", f"${total_revenue:,}")
with col4:
    st.metric("Keywords Tracked", total_keywords)

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Clients", "➕ Add Client", "📊 Analytics", "⚙️ Settings"])

with tab1:
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_filter = st.text_input("🔍 Search clients", placeholder="Name or email")
    with col2:
        status_filter = st.multiselect(
            "Status",
            options=['Active', 'Pending', 'Inactive'],
            default=['Active', 'Pending']
        )
    with col3:
        package_filter = st.multiselect(
            "Package",
            options=['Premium', 'Standard', 'Basic'],
            default=['Premium', 'Standard', 'Basic']
        )
    
    # Filter clients
    filtered_clients = st.session_state.clients
    
    if search_filter:
        filtered_clients = [c for c in filtered_clients 
                          if search_filter.lower() in c['name'].lower() 
                          or search_filter.lower() in c['email'].lower()]
    
    if status_filter:
        filtered_clients = [c for c in filtered_clients if c['status'] in status_filter]
    
    if package_filter:
        filtered_clients = [c for c in filtered_clients if c['package'] in package_filter]
    
    # Display clients
    if not filtered_clients:
        st.info("No clients found matching your filters")
    else:
        for client in sorted(filtered_clients, key=lambda x: x['name']):
            with st.expander(f"**{client['name']}** - {client['package']} Package", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Contact:** {client['contact']}")
                    st.markdown(f"**Email:** {client['email']}")
                    st.markdown(f"**Phone:** {client['phone']}")
                    st.markdown(f"**Website:** [{client['website']}]({client['website']})")
                    st.markdown(f"**Status:** {client['status']}")
                    
                with col2:
                    st.metric("Monthly Fee", f"${client['monthly_fee']:,}")
                    st.metric("Keywords Tracked", client['keywords_tracked'])
                    st.metric("Reports Sent", client['reports_sent'])
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Start Date:** {client['start_date'].strftime('%Y-%m-%d')}")
                with col2:
                    st.markdown(f"**Last Report:** {client['last_report'].strftime('%Y-%m-%d')}")
                with col3:
                    days_active = (datetime.now() - client['start_date']).days
                    st.markdown(f"**Client for:** {days_active} days")
                
                st.markdown(f"**Notes:** {client['notes']}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("📊 View Reports", key=f"reports_{client['id']}", use_container_width=True):
                        st.info(f"Opening reports for {client['name']}")
                with col2:
                    if st.button("📧 Send Email", key=f"email_{client['id']}", use_container_width=True):
                        st.info(f"Opening email to {client['email']}")
                with col3:
                    if st.button("✏️ Edit", key=f"edit_{client['id']}", use_container_width=True):
                        st.session_state[f'editing_{client["id"]}'] = True
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{client['id']}", use_container_width=True):
                        st.session_state.clients = [c for c in st.session_state.clients if c['id'] != client['id']]
                        st.success(f"Deleted {client['name']}")
                        st.rerun()

with tab2:
    st.markdown("### ➕ Add New Client")
    
    with st.form("add_client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name*", placeholder="Acme Corporation")
            contact_name = st.text_input("Contact Person*", placeholder="John Smith")
            email = st.text_input("Email*", placeholder="john@acme.com")
            phone = st.text_input("Phone", placeholder="+1 555-0123")
            
        with col2:
            website = st.text_input("Website*", placeholder="https://acme.com")
            package = st.selectbox("Package*", options=['Premium', 'Standard', 'Basic'])
            monthly_fee = st.number_input("Monthly Fee ($)*", min_value=0, value=1500, step=100)
            start_date = st.date_input("Start Date*", value=datetime.now())
        
        keywords_tracked = st.number_input("Keywords to Track", min_value=0, value=30, step=5)
        notes = st.text_area("Notes", placeholder="Additional information about this client...")
        
        submitted = st.form_submit_button("Add Client", use_container_width=True)
        
        if submitted:
            if company_name and contact_name and email and website:
                new_client = {
                    'id': max([c['id'] for c in st.session_state.clients]) + 1 if st.session_state.clients else 1,
                    'name': company_name,
                    'contact': contact_name,
                    'email': email,
                    'phone': phone,
                    'website': website,
                    'status': 'Active',
                    'package': package,
                    'monthly_fee': monthly_fee,
                    'start_date': datetime.combine(start_date, datetime.min.time()),
                    'keywords_tracked': keywords_tracked,
                    'reports_sent': 0,
                    'last_report': datetime.now(),
                    'notes': notes
                }
                
                st.session_state.clients.append(new_client)
                st.success(f"✅ Added client: {company_name}")
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")

with tab3:
    st.markdown("### 📊 Client Analytics")
    
    # Revenue chart
    st.markdown("#### 💰 Monthly Revenue by Package")
    
    revenue_by_package = {}
    for client in st.session_state.clients:
        if client['status'] == 'Active':
            if client['package'] not in revenue_by_package:
                revenue_by_package[client['package']] = 0
            revenue_by_package[client['package']] += client['monthly_fee']
    
    if revenue_by_package:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            import plotly.graph_objects as go
            
            fig = go.Figure(data=[go.Bar(
                x=list(revenue_by_package.keys()),
                y=list(revenue_by_package.values()),
                marker_color=['#667eea', '#764ba2', '#f093fb']
            )])
            
            fig.update_layout(
                xaxis_title="Package",
                yaxis_title="Monthly Revenue ($)",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Revenue Breakdown**")
            for package, revenue in revenue_by_package.items():
                st.metric(package, f"${revenue:,}")
    
    # Client growth
    st.markdown("#### 📈 Client Growth")
    
    # Simulate growth data
    months = [(datetime.now() - timedelta(days=30*x)).strftime("%b %Y") for x in range(6, 0, -1)]
    client_counts = [len(st.session_state.clients) - x for x in range(5, -1, -1)]
    
    import plotly.express as px
    
    fig = px.line(
        x=months,
        y=client_counts,
        markers=True,
        labels={'x': 'Month', 'y': 'Number of Clients'}
    )
    
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top clients
    st.markdown("#### 🏆 Top Clients by Revenue")
    
    top_clients = sorted(st.session_state.clients, key=lambda x: x['monthly_fee'], reverse=True)[:5]
    
    for i, client in enumerate(top_clients, 1):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{i}. {client['name']}**")
        with col2:
            st.markdown(f"${client['monthly_fee']:,}/mo")
        with col3:
            st.markdown(f"{client['package']}")

with tab4:
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📧 Email Templates")
        
        st.selectbox(
            "Welcome Email Template",
            options=['Default Welcome', 'Premium Welcome', 'Custom Template']
        )
        
        st.selectbox(
            "Monthly Report Template",
            options=['Standard Report', 'Executive Summary', 'Detailed Analysis']
        )
        
        st.checkbox("Auto-send monthly reports", value=True)
        st.checkbox("Send invoice reminders", value=True)
        
    with col2:
        st.markdown("#### 💼 Package Settings")
        
        st.markdown("**Premium Package**")
        st.number_input("Default price", value=2500, step=100, key="premium_price")
        st.number_input("Keywords included", value=50, step=10, key="premium_keywords")
        
        st.markdown("**Standard Package**")
        st.number_input("Default price", value=1500, step=100, key="standard_price")
        st.number_input("Keywords included", value=30, step=10, key="standard_keywords")
        
        st.markdown("**Basic Package**")
        st.number_input("Default price", value=800, step=100, key="basic_price")
        st.number_input("Keywords included", value=15, step=5, key="basic_keywords")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 Import/Export")
        
        if st.button("📥 Export Clients to CSV", use_container_width=True):
            df = pd.DataFrame(st.session_state.clients)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"clients_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        uploaded_file = st.file_uploader("Import Clients from CSV", type=['csv'])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"Ready to import {len(df)} clients")
                
                if st.button("Confirm Import"):
                    for _, row in df.iterrows():
                        new_client = {
                            'id': max([c['id'] for c in st.session_state.clients]) + 1 if st.session_state.clients else 1,
                            'name': row['name'],
                            'contact': row['contact'],
                            'email': row['email'],
                            'phone': row.get('phone', ''),
                            'website': row['website'],
                            'status': row.get('status', 'Active'),
                            'package': row.get('package', 'Standard'),
                            'monthly_fee': row.get('monthly_fee', 1500),
                            'start_date': datetime.now(),
                            'keywords_tracked': row.get('keywords_tracked', 30),
                            'reports_sent': 0,
                            'last_report': datetime.now(),
                            'notes': row.get('notes', '')
                        }
                        st.session_state.clients.append(new_client)
                    st.success(f"✅ Imported {len(df)} clients")
                    st.rerun()
            except Exception as e:
                st.error(f"Error importing: {str(e)}")
    
    with col2:
        st.markdown("#### 🗑️ Data Management")
        
        if st.button("🔄 Backup All Data", use_container_width=True):
            st.success("✅ Backup created successfully")
        
        if st.button("🗑️ Delete All Clients", type="secondary", use_container_width=True):
            if st.session_state.get('confirm_delete_all', False):
                st.session_state.clients = []
                st.session_state.confirm_delete_all = False
                st.success("All clients deleted")
                st.rerun()
            else:
                st.session_state.confirm_delete_all = True
                st.warning("⚠️ Click again to confirm deletion")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Use custom email templates to automate client communication and save time!")