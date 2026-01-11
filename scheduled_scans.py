"""
Scheduled Scans - Automate Your SEO Monitoring
Set up recurring scans to monitor your sites automatically
"""

import streamlit as st
from datetime import datetime, timedelta, time
import random

# Page config
st.set_page_config(page_title="Scheduled Scans", page_icon="⏰", layout="wide")

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
    .schedule-card {
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
    .status-paused {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'schedules' not in st.session_state:
    st.session_state.schedules = [
        {
            'id': 1,
            'name': 'Daily Homepage Check',
            'url': 'https://example.com',
            'frequency': 'Daily',
            'time': '09:00',
            'scan_type': 'Quick Scan',
            'status': 'Active',
            'last_run': datetime.now() - timedelta(days=1),
            'next_run': datetime.now() + timedelta(days=1),
            'runs_completed': 45,
            'notifications': True
        },
        {
            'id': 2,
            'name': 'Weekly Full Audit',
            'url': 'https://example.com',
            'frequency': 'Weekly',
            'time': '02:00',
            'scan_type': 'Full Audit',
            'status': 'Active',
            'last_run': datetime.now() - timedelta(days=7),
            'next_run': datetime.now() + timedelta(days=7),
            'runs_completed': 12,
            'notifications': True
        }
    ]

if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# Header
st.markdown('<div class="main-header">⏰ Scheduled Scans</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automate your SEO monitoring with recurring scans</div>', unsafe_allow_html=True)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

active_schedules = sum(1 for s in st.session_state.schedules if s['status'] == 'Active')
total_runs = sum(s['runs_completed'] for s in st.session_state.schedules)
next_scan = min(s['next_run'] for s in st.session_state.schedules) if st.session_state.schedules else datetime.now()

with col1:
    st.metric("Active Schedules", active_schedules)
with col2:
    st.metric("Total Scans Run", total_runs)
with col3:
    hours_until_next = (next_scan - datetime.now()).total_seconds() / 3600
    st.metric("Next Scan In", f"{hours_until_next:.1f}h")
with col4:
    st.metric("This Month", random.randint(100, 200))

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📅 Schedules", "➕ New Schedule", "📊 History", "⚙️ Settings"])

with tab1:
    st.markdown("### 📅 Your Scheduled Scans")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            options=['Active', 'Paused'],
            default=['Active', 'Paused']
        )
    
    with col2:
        frequency_filter = st.multiselect(
            "Frequency",
            options=['Daily', 'Weekly', 'Monthly'],
            default=['Daily', 'Weekly', 'Monthly']
        )
    
    with col3:
        scan_type_filter = st.multiselect(
            "Scan Type",
            options=['Quick Scan', 'Full Audit', 'Custom'],
            default=['Quick Scan', 'Full Audit', 'Custom']
        )
    
    # Filter schedules
    filtered_schedules = st.session_state.schedules
    
    if status_filter:
        filtered_schedules = [s for s in filtered_schedules if s['status'] in status_filter]
    
    if frequency_filter:
        filtered_schedules = [s for s in filtered_schedules if s['frequency'] in frequency_filter]
    
    if scan_type_filter:
        filtered_schedules = [s for s in filtered_schedules if s['scan_type'] in scan_type_filter]
    
    # Display schedules
    if not filtered_schedules:
        st.info("No schedules found. Create your first schedule!")
    else:
        for schedule in sorted(filtered_schedules, key=lambda x: x['next_run']):
            with st.expander(f"**{schedule['name']}** - {schedule['frequency']} at {schedule['time']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**URL:** {schedule['url']}")
                    st.markdown(f"**Scan Type:** {schedule['scan_type']}")
                    st.markdown(f"**Frequency:** {schedule['frequency']} at {schedule['time']}")
                    st.markdown(f"**Status:** {schedule['status']}")
                    
                with col2:
                    st.metric("Runs Completed", schedule['runs_completed'])
                    st.markdown(f"**Last Run:** {schedule['last_run'].strftime('%Y-%m-%d %H:%M')}")
                    st.markdown(f"**Next Run:** {schedule['next_run'].strftime('%Y-%m-%d %H:%M')}")
                
                st.markdown("---")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if schedule['status'] == 'Active':
                        if st.button("⏸️ Pause", key=f"pause_{schedule['id']}", use_container_width=True):
                            schedule['status'] = 'Paused'
                            st.success("Schedule paused")
                            st.rerun()
                    else:
                        if st.button("▶️ Resume", key=f"resume_{schedule['id']}", use_container_width=True):
                            schedule['status'] = 'Active'
                            st.success("Schedule resumed")
                            st.rerun()
                
                with col2:
                    if st.button("🚀 Run Now", key=f"run_{schedule['id']}", use_container_width=True):
                        with st.spinner("Running scan..."):
                            import time
                            time.sleep(2)
                            schedule['runs_completed'] += 1
                            schedule['last_run'] = datetime.now()
                            st.success("✅ Scan completed!")
                            st.rerun()
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_{schedule['id']}", use_container_width=True):
                        st.session_state[f'editing_{schedule["id"]}'] = True
                        st.info("Edit mode enabled")
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{schedule['id']}", use_container_width=True):
                        st.session_state.schedules = [s for s in st.session_state.schedules if s['id'] != schedule['id']]
                        st.success("Schedule deleted")
                        st.rerun()
                
                # Email notifications
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.checkbox(
                        "📧 Email notifications", 
                        value=schedule['notifications'],
                        key=f"notif_{schedule['id']}"
                    )
                
                with col2:
                    if schedule['notifications']:
                        st.text_input(
                            "Email recipients",
                            value="you@example.com",
                            key=f"email_{schedule['id']}"
                        )

with tab2:
    st.markdown("### ➕ Create New Schedule")
    
    with st.form("create_schedule_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            schedule_name = st.text_input("Schedule Name*", placeholder="Daily Homepage Check")
            url_to_scan = st.text_input("URL to Scan*", placeholder="https://example.com")
            scan_type = st.selectbox(
                "Scan Type*",
                options=['Quick Scan', 'Full Audit', 'Custom']
            )
            
            if scan_type == 'Custom':
                st.multiselect(
                    "Select checks to include",
                    options=[
                        'Meta Tags',
                        'Headings',
                        'Images',
                        'Links',
                        'Performance',
                        'Mobile Usability',
                        'Schema Markup',
                        'Security'
                    ],
                    default=['Meta Tags', 'Headings', 'Links']
                )
        
        with col2:
            frequency = st.selectbox(
                "Frequency*",
                options=['Daily', 'Weekly', 'Monthly', 'Custom']
            )
            
            if frequency == 'Custom':
                custom_interval = st.number_input("Run every", min_value=1, value=3)
                custom_unit = st.selectbox("Unit", options=['Hours', 'Days', 'Weeks'])
            
            if frequency == 'Weekly':
                day_of_week = st.selectbox(
                    "Day of Week",
                    options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                )
            
            if frequency == 'Monthly':
                day_of_month = st.number_input("Day of Month", min_value=1, max_value=31, value=1)
            
            scan_time = st.time_input("Time to Run*", value=time(9, 0))
        
        st.markdown("#### 🔔 Notifications")
        
        col1, col2 = st.columns(2)
        
        with col1:
            enable_notifications = st.checkbox("Enable email notifications", value=True)
            notify_success = st.checkbox("Notify on successful scan", value=False)
            notify_failure = st.checkbox("Notify on scan failure", value=True)
        
        with col2:
            notify_issues = st.checkbox("Notify on new issues found", value=True)
            notify_improvements = st.checkbox("Notify on improvements", value=True)
            
            if enable_notifications:
                notification_email = st.text_input("Notification Email", placeholder="you@example.com")
        
        st.markdown("#### ⚙️ Advanced Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_pages = st.number_input("Max pages to scan", min_value=1, value=100, step=10)
            timeout = st.number_input("Timeout (seconds)", min_value=10, value=60, step=10)
        
        with col2:
            user_agent = st.selectbox(
                "User Agent",
                options=['Desktop', 'Mobile', 'Tablet', 'Googlebot']
            )
            follow_redirects = st.checkbox("Follow redirects", value=True)
        
        submitted = st.form_submit_button("Create Schedule", type="primary", use_container_width=True)
        
        if submitted:
            if schedule_name and url_to_scan:
                new_schedule = {
                    'id': max([s['id'] for s in st.session_state.schedules]) + 1 if st.session_state.schedules else 1,
                    'name': schedule_name,
                    'url': url_to_scan,
                    'frequency': frequency,
                    'time': scan_time.strftime('%H:%M'),
                    'scan_type': scan_type,
                    'status': 'Active',
                    'last_run': None,
                    'next_run': datetime.now() + timedelta(days=1),
                    'runs_completed': 0,
                    'notifications': enable_notifications
                }
                
                st.session_state.schedules.append(new_schedule)
                st.success(f"✅ Schedule '{schedule_name}' created successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")

with tab3:
    st.markdown("### 📊 Scan History")
    
    # Generate sample history
    sample_history = []
    for schedule in st.session_state.schedules:
        for i in range(min(schedule['runs_completed'], 10)):
            sample_history.append({
                'schedule': schedule['name'],
                'url': schedule['url'],
                'date': schedule['last_run'] - timedelta(days=i),
                'status': random.choice(['Success', 'Success', 'Success', 'Warning']),
                'duration': f"{random.randint(10, 300)}s",
                'issues_found': random.randint(0, 15),
                'score': random.randint(70, 100)
            })
    
    sample_history.sort(key=lambda x: x['date'], reverse=True)
    
    # Filters
    col1, col2 = st.columns([3, 1])
    
    with col1:
        schedule_filter = st.multiselect(
            "Filter by Schedule",
            options=list(set(h['schedule'] for h in sample_history)),
            default=list(set(h['schedule'] for h in sample_history))
        )
    
    with col2:
        status_filter_history = st.selectbox(
            "Status",
            options=['All', 'Success', 'Warning', 'Error']
        )
    
    # Filter history
    filtered_history = sample_history
    
    if schedule_filter:
        filtered_history = [h for h in filtered_history if h['schedule'] in schedule_filter]
    
    if status_filter_history != 'All':
        filtered_history = [h for h in filtered_history if h['status'] == status_filter_history]
    
    # Display history
    if filtered_history:
        st.markdown(f"Showing {len(filtered_history)} scans")
        
        for scan in filtered_history[:20]:  # Show last 20
            status_color = {
                'Success': '🟢',
                'Warning': '🟡',
                'Error': '🔴'
            }
            
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{scan['schedule']}**")
            with col2:
                st.markdown(f"{scan['date'].strftime('%Y-%m-%d %H:%M')}")
            with col3:
                st.markdown(f"{status_color[scan['status']]} {scan['status']}")
            with col4:
                st.markdown(f"⏱️ {scan['duration']}")
            with col5:
                st.markdown(f"⚠️ {scan['issues_found']}")
            with col6:
                st.markdown(f"📊 {scan['score']}/100")
            
            st.markdown("---")
    else:
        st.info("No scan history available")
    
    # Charts
    if sample_history:
        st.markdown("### 📈 Scan Performance")
        
        import plotly.graph_objects as go
        
        # Issues over time
        dates = [h['date'].strftime('%Y-%m-%d') for h in sample_history[:30]]
        issues = [h['issues_found'] for h in sample_history[:30]]
        scores = [h['score'] for h in sample_history[:30]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=issues,
            mode='lines+markers',
            name='Issues Found',
            yaxis='y',
            line=dict(color='#ef4444', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=scores,
            mode='lines+markers',
            name='SEO Score',
            yaxis='y2',
            line=dict(color='#10b981', width=2)
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis=dict(title="Issues Found", side='left'),
            yaxis2=dict(title="SEO Score", side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### ⚙️ Schedule Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔔 Global Notifications")
        
        enable_all_notifications = st.checkbox("Enable all notifications", value=True)
        
        st.markdown("**Email Settings**")
        default_email = st.text_input("Default notification email", value="you@example.com")
        
        st.multiselect(
            "Notification triggers",
            options=[
                'Scan completed',
                'Scan failed',
                'New issues found',
                'Issues resolved',
                'Score improved',
                'Score decreased'
            ],
            default=['Scan failed', 'New issues found', 'Score decreased']
        )
        
        st.markdown("#### 🕐 Default Schedule Settings")
        
        default_time = st.time_input("Default scan time", value=time(9, 0))
        default_timeout = st.number_input("Default timeout (seconds)", min_value=10, value=60, step=10)
        default_max_pages = st.number_input("Default max pages", min_value=1, value=100, step=10)
    
    with col2:
        st.markdown("#### 🔄 Retry Settings")
        
        enable_retry = st.checkbox("Auto-retry failed scans", value=True)
        
        if enable_retry:
            retry_attempts = st.number_input("Max retry attempts", min_value=1, max_value=5, value=3)
            retry_delay = st.number_input("Delay between retries (minutes)", min_value=1, value=15)
        
        st.markdown("#### 🗑️ History Settings")
        
        history_retention = st.selectbox(
            "Keep scan history for",
            options=['30 days', '90 days', '180 days', '1 year', 'Forever']
        )
        
        auto_delete_old = st.checkbox("Auto-delete old scans", value=True)
        
        st.markdown("#### 💾 Backup")
        
        if st.button("📥 Export All Schedules", use_container_width=True):
            import pandas as pd
            df = pd.DataFrame(st.session_state.schedules)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"schedules_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if st.button("🗑️ Delete All Schedules", type="secondary", use_container_width=True):
            if st.session_state.get('confirm_delete_schedules', False):
                st.session_state.schedules = []
                st.session_state.confirm_delete_schedules = False
                st.success("All schedules deleted")
                st.rerun()
            else:
                st.session_state.confirm_delete_schedules = True
                st.warning("⚠️ Click again to confirm")
    
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.success("✅ Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Set up daily scans to catch issues early and weekly full audits for comprehensive monitoring!")
