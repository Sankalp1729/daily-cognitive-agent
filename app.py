import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random

from cognitive_agent import CognitiveAgent
from email_simulator import EmailSimulator
from steganography import SteganographyModule
from email_fetcher import RealEmailFetcher

# Page configuration
st.set_page_config(
    page_title="Daily Cognitive Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = CognitiveAgent()

if 'email_simulator' not in st.session_state:
    st.session_state.email_simulator = EmailSimulator()

if 'steganography' not in st.session_state:
    st.session_state.steganography = SteganographyModule()

if 'current_email' not in st.session_state:
    st.session_state.current_email = None

if 'stealth_logs' not in st.session_state:
    st.session_state.stealth_logs = []

if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = []

if 'email_fetcher' not in st.session_state:
    st.session_state.email_fetcher = None

if 'use_real_emails' not in st.session_state:
    st.session_state.use_real_emails = False

if 'fetched_emails' not in st.session_state:
    st.session_state.fetched_emails = []

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .inbox-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .inbox-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    .prediction-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .prediction-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 2px;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .prediction-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .action-prediction {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
        display: inline-block;
        margin: 1rem 0;
        text-align: center;
        width: 100%;
    }
    
    .confidence-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .confidence-label {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .explanation-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
        font-style: italic;
        font-size: 1.1rem;
        line-height: 1.6;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .feedback-button-container {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .approve-button {
        background: linear-gradient(135deg, #00d4aa 0%, #01a085 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.3);
    }
    
    .approve-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 212, 170, 0.4);
    }
    
    .reject-button {
        background: linear-gradient(135deg, #ef5350 0%, #d32f2f 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 6px 20px rgba(239, 83, 80, 0.3);
    }
    
    .reject-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(239, 83, 80, 0.4);
    }
    
    .correction-button {
        background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 167, 38, 0.3);
    }
    
    .correction-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 167, 38, 0.4);
    }
    
    .email-metadata {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #4caf50;
        font-family: 'Inter', sans-serif;
    }
    
    .email-metadata strong {
        color: #2e7d32;
        font-weight: 600;
    }
    
    .priority-high {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #f44336;
        color: #c62828;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        border-left: 5px solid #ff9800;
        color: #ef6c00;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        color: #2e7d32;
    }
    
    .real-email-badge {
        background: linear-gradient(135deg, #00d4aa 0%, #01a085 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        display: inline-block;
        margin-left: 1rem;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    .no-email-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        margin: 2rem 0;
    }
    
    .no-email-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.8;
    }
    
    .no-email-text {
        font-size: 1.3rem;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
    }
    
    .dashboard-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
        margin: 1rem 0;
    }
    
    .performance-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        margin: 1rem 0;
    }
    
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .email-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e3f2fd;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .email-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .email-card h4 {
        font-family: 'Poppins', sans-serif;
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .email-card p {
        font-family: 'Inter', sans-serif;
        color: #34495e;
        font-size: 1rem;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    
    .email-card strong {
        color: #2c3e50;
        font-weight: 600;
    }
    
    .confidence-high {
        color: #00d4aa;
        font-weight: 700;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(0, 212, 170, 0.3);
    }
    
    .confidence-medium {
        color: #ffa726;
        font-weight: 700;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(255, 167, 38, 0.3);
    }
    
    .confidence-low {
        color: #ef5350;
        font-weight: 700;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(239, 83, 80, 0.3);
    }
    
    .action-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .feedback-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .sender-info {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #2196f3;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
    }
    
    .subject-line {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .email-body {
        background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    .no-data-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .no-data-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
    
    .no-data-text {
        font-size: 1.2rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .performance-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .trend-indicator {
        font-size: 1.2rem;
        margin-left: 0.5rem;
    }
    
    .trend-up {
        color: #00d4aa;
    }
    
    .trend-down {
        color: #ef5350;
    }
    
    .trend-stable {
        color: #ffa726;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Daily Cognitive Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Agent Controls")
        
        # Real Email Connection
        st.subheader("📧 Email Source")
        use_real_emails = st.checkbox("🔗 Connect to Real Gmail", value=st.session_state.use_real_emails)
        
        if use_real_emails:
            st.session_state.use_real_emails = True
            
            # Gmail App Password input
            app_password = st.text_input("🔑 Gmail App Password", type="password", 
                                       help="Enter your Gmail App Password (not regular password)")
            
            if app_password:
                if st.session_state.email_fetcher is None:
                    st.session_state.email_fetcher = RealEmailFetcher("blackhole01729@gmail.com", app_password)
                
                # Test connection
                if st.button("🔗 Test Connection", use_container_width=True):
                    if st.session_state.email_fetcher.connect():
                        st.success("✅ Connected to Gmail successfully!")
                        st.session_state.email_fetcher.disconnect()
                    else:
                        st.error("❌ Failed to connect. Check your App Password.")
                
                # Fetch real emails
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📬 Fetch Recent Emails", use_container_width=True):
                        with st.spinner("📥 Fetching recent emails from Gmail..."):
                            emails = st.session_state.email_fetcher.fetch_recent_emails(10)
                            if emails:
                                st.session_state.fetched_emails = emails
                                st.success(f"✅ Fetched {len(emails)} recent emails!")
                                st.rerun()
                            else:
                                st.error("❌ No emails found or connection failed.")
                
                with col2:
                    # Search by sender
                    sender_search = st.text_input("🔍 Search by sender email:", placeholder="e.g., support@company.com")
                    if st.button("🔍 Search Sender", use_container_width=True):
                        if sender_search:
                            with st.spinner(f"📥 Searching emails from {sender_search}..."):
                                emails = st.session_state.email_fetcher.fetch_emails_by_sender(sender_search, 10)
                                if emails:
                                    st.session_state.fetched_emails = emails
                                    st.success(f"✅ Found {len(emails)} emails from {sender_search}!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ No emails found from {sender_search}")
                        else:
                            st.error("❌ Please enter a sender email address")
                
                # Email selection
                if st.session_state.fetched_emails:
                    st.subheader(f"📧 Select Email to Analyze ({len(st.session_state.fetched_emails)} emails available)")
                    
                    # Refresh button
                    if st.button("🔄 Refresh Email List", use_container_width=True):
                        with st.spinner("📥 Refreshing emails..."):
                            emails = st.session_state.email_fetcher.fetch_recent_emails(10)
                            if emails:
                                st.session_state.fetched_emails = emails
                                st.success(f"✅ Refreshed! {len(emails)} emails available.")
                                st.rerun()
                            else:
                                st.error("❌ Failed to refresh emails.")
                    
                    # Create email options for selection
                    email_options = []
                    for i, email in enumerate(st.session_state.fetched_emails):
                        # Truncate subject if too long
                        subject = email['subject'][:50] + "..." if len(email['subject']) > 50 else email['subject']
                        option_text = f"{i+1}. {subject} - {email['sender']}"
                        email_options.append((option_text, i))
                    
                    # Email selection dropdown
                    selected_option = st.selectbox(
                        "Choose an email:",
                        options=[opt[0] for opt in email_options],
                        index=0
                    )
                    
                    # Get selected email index
                    selected_index = next(opt[1] for opt in email_options if opt[0] == selected_option)
                    selected_email = st.session_state.fetched_emails[selected_index]
                    
                    # Show selected email preview
                    st.markdown(f"**Selected:** {selected_email['subject']}")
                    st.markdown(f"**From:** {selected_email['sender']}")
                    st.markdown(f"**Time:** {selected_email['timestamp'][:19]}")
                    
                    # Analyze selected email button
                    if st.button("🔍 Analyze Selected Email", use_container_width=True):
                        st.session_state.current_email = selected_email
                        
                        # Get agent prediction
                        prediction = st.session_state.agent.predict_action(st.session_state.current_email)
                        
                        # Generate stealth log
                        stealth_entry = st.session_state.steganography.generate_stealth_log(
                            st.session_state.current_email,
                            prediction
                        )
                        st.session_state.stealth_logs.append(stealth_entry)
                        
                        st.success("✅ Email analyzed! Check the main area for results.")
                        st.rerun()
                    
                    # Clear fetched emails
                    if st.button("🗑️ Clear Fetched Emails", use_container_width=True):
                        st.session_state.fetched_emails = []
                        st.session_state.current_email = None
                        st.success("✅ Cleared fetched emails!")
                        st.rerun()
        else:
            st.session_state.use_real_emails = False
            st.session_state.email_fetcher = None
        
        st.divider()
        
        # Generate simulated email
        if st.button("🎲 Generate Simulated Email", use_container_width=True):
            # Generate email with higher chance of blackhole01729@gmail.com
            if random.random() < 0.3:  # 30% chance
                email_types = ["urgent", "question", "newsletter"]
                email_type = random.choice(email_types)
                st.session_state.current_email = st.session_state.email_simulator.generate_specific_email(
                    sender="blackhole01729@gmail.com",
                    subject_type=email_type
                )
            else:
                st.session_state.current_email = st.session_state.email_simulator.generate_email()
            
            # Get agent prediction
            prediction = st.session_state.agent.predict_action(st.session_state.current_email)
            
            # Generate stealth log
            stealth_entry = st.session_state.steganography.generate_stealth_log(
                st.session_state.current_email,
                prediction
            )
            st.session_state.stealth_logs.append(stealth_entry)
            
            st.rerun()
        
        # Generate multiple emails
        if st.button("📬 Generate Inbox (10 emails)", use_container_width=True):
            inbox = st.session_state.email_simulator.generate_inbox(10)
            for email in inbox:
                prediction = st.session_state.agent.predict_action(email)
                stealth_entry = st.session_state.steganography.generate_stealth_log(email, prediction)
                st.session_state.stealth_logs.append(stealth_entry)
            st.rerun()
        
        st.divider()
        
        # Agent settings
        st.subheader("🤖 Agent Settings")
        learning_rate = st.slider("Learning Rate", 0.01, 0.5, st.session_state.agent.learning_rate, 0.01)
        epsilon = st.slider("Exploration Rate (Epsilon)", 0.0, 1.0, st.session_state.agent.epsilon, 0.05)
        
        if learning_rate != st.session_state.agent.learning_rate or epsilon != st.session_state.agent.epsilon:
            st.session_state.agent.learning_rate = learning_rate
            st.session_state.agent.epsilon = epsilon
        
        # Statistics
        stats = st.session_state.agent.get_statistics()
        st.subheader("📊 Quick Stats")
        st.metric("Total Feedback", stats['total_feedback'])
        st.metric("Approval Rate", f"{stats['approval_rate']:.1%}")
        st.metric("Avg Confidence", f"{stats['avg_confidence']:.3f}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="inbox-header">📧 Inbox Simulator</div>', unsafe_allow_html=True)
        
        if st.session_state.current_email:
            display_email_card(st.session_state.current_email)
        else:
            st.markdown("""
            <div class="no-email-card">
                <div class="no-email-icon">📧</div>
                <div class="no-email-text">Click 'Generate New Email' to start!</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="prediction-header">🤖 Agent Prediction</div>', unsafe_allow_html=True)
        
        if st.session_state.current_email:
            # Get latest prediction
            prediction = st.session_state.agent.predict_action(st.session_state.current_email)
            display_prediction_card(prediction)
        else:
            st.markdown("""
            <div class="no-email-card">
                <div class="no-email-icon">🤖</div>
                <div class="no-email-text">No email to analyze</div>
            </div>
            """, unsafe_allow_html=True)

def format_email_body(body_text):
    """Format and clean email body text"""
    if not body_text:
        return "No content available"
    
    # Remove HTML-like tags and clean up the text
    import re
    
    # Remove HTML tags
    body_text = re.sub(r'<[^>]+>', '', body_text)
    
    # Remove common email artifacts
    body_text = re.sub(r'\[image:.*?\]', '', body_text)  # Remove image placeholders
    body_text = re.sub(r'\[.*?\]', '', body_text)  # Remove other brackets
    
    # Clean up URLs (make them readable)
    body_text = re.sub(r'https?://[^\s]+', lambda m: f"🔗 {m.group(0)}", body_text)
    
    # Clean up excessive whitespace
    body_text = re.sub(r'\n\s*\n', '\n\n', body_text)  # Remove excessive line breaks
    body_text = re.sub(r' +', ' ', body_text)  # Remove multiple spaces
    
    # Clean up the text
    body_text = body_text.strip()
    
    # Add some formatting for better readability
    lines = body_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            # Make important lines stand out
            if any(keyword in line.lower() for keyword in ['urgent', 'important', 'action required', 'security']):
                line = f"⚠️ {line}"
            elif any(keyword in line.lower() for keyword in ['password', 'account', 'login']):
                line = f"🔐 {line}"
            elif any(keyword in line.lower() for keyword in ['http', 'www']):
                line = f"🔗 {line}"
            
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def display_email_card(email):
    """Display email information in a card format"""
    # Color coding for priority
    priority_colors = {
        'high': '🔴',
        'medium': '🟡', 
        'low': '🟢'
    }
    priority_icon = priority_colors.get(email['priority'], '⚪')
    
    # Check if this is a real email
    is_real_email = email.get('real_email', False)
    
    # Create the email card using Streamlit components
    with st.container():
        st.markdown("---")
        
        # Subject line
        subject_col1, subject_col2 = st.columns([4, 1])
        with subject_col1:
            st.markdown(f"### 📧 {email['subject']}")
        with subject_col2:
            if is_real_email:
                st.success("🔗 REAL EMAIL")
        
        # Email metadata
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**👤 From:** {email['sender']}")
            st.markdown(f"**🕒 Time:** {email['timestamp'][:19]}")
        
        with col2:
            st.markdown(f"**📊 Priority:** {priority_icon} {email['priority'].title()}")
            st.markdown(f"**📎 Attachments:** {len(email['attachments'])}")
        
        # Message ID for real emails
        if is_real_email:
            st.code(f"Message ID: {email.get('message_id', 'N/A')}", language="text")
        
        # Email body
        with st.expander("📄 Email Body", expanded=False):
            formatted_body = format_email_body(email['body'])
            st.text_area("Email Content", value=formatted_body, height=200, disabled=True, label_visibility="collapsed")
        
        st.markdown("---")

def display_prediction_card(prediction):
    """Display agent prediction with confidence and explanation"""
    action = prediction['action']
    confidence = prediction['confidence']
    explanation = prediction['explanation']
    
    # Confidence color and icon
    if confidence > 0.7:
        conf_color = "🟢"
        conf_status = "High"
    elif confidence > 0.4:
        conf_color = "🟡"
        conf_status = "Medium"
    else:
        conf_color = "🔴"
        conf_status = "Low"
    
    # Create prediction card using Streamlit components
    with st.container():
        st.markdown("---")
        st.markdown("### 🎯 Agent Prediction")
        
        # Action badge
        st.markdown(f"**Predicted Action:**")
        st.info(f"**{action}**")
        
        # Confidence level
        st.markdown(f"**Confidence Level:** {conf_color} {conf_status} ({confidence:.3f})")
        
        # AI Explanation
        st.markdown("**🤖 AI Explanation:**")
        st.markdown(f"*{explanation}*")
        
        st.markdown("---")
    
    # Feedback buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("👍 Approve", use_container_width=True, type="primary"):
            handle_feedback('approve')
    
    with col2:
        if st.button("👎 Reject", use_container_width=True):
            handle_feedback('reject')
    
    with col3:
        # Action correction dropdown
        correct_action = st.selectbox(
            "Correct Action:",
            st.session_state.agent.actions,
            index=st.session_state.agent.actions.index(prediction['action'])
        )
        
        if st.button("✅ Submit Correction", use_container_width=True):
            handle_feedback('reject', correct_action)

def handle_feedback(feedback_type, correct_action=None):
    """Handle user feedback and update agent"""
    if st.session_state.current_email:
        # Get current prediction
        prediction = st.session_state.agent.predict_action(st.session_state.current_email)
        
        # Update agent with feedback
        feedback_entry = st.session_state.agent.receive_feedback(
            st.session_state.current_email,
            prediction['action'],
            feedback_type,
            correct_action
        )
        
        # Add to feedback history
        st.session_state.feedback_history.append(feedback_entry)
        
        # Show success message
        if feedback_type == 'approve':
            st.success("✅ Feedback recorded! Agent learning from approval.")
        else:
            st.success("✅ Feedback recorded! Agent learning from correction.")
        
        # Clear current email
        st.session_state.current_email = None
        time.sleep(1)
        st.rerun()

def show_dashboard():
    """Show the feedback dashboard with visualizations"""
    st.markdown('<h1 class="dashboard-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    stats = st.session_state.agent.get_statistics()
    
    if stats['total_feedback'] == 0:
        st.markdown("""
        <div class="no-data-card">
            <div class="no-data-icon">📈</div>
            <div class="no-data-text">No feedback data available yet.<br>Start interacting with emails to see beautiful analytics!</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced Metrics Section
    st.markdown('<h2 class="section-header">📊 Key Performance Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate trend indicators
    approval_trend = "📈" if stats['approval_rate'] > 0.7 else "📉" if stats['approval_rate'] < 0.3 else "➡️"
    confidence_trend = "📈" if stats['avg_confidence'] > 0.6 else "📉" if stats['avg_confidence'] < 0.4 else "➡️"
    
    # Metrics Grid with Icons and Colors
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-value">{stats['total_feedback']}</div>
            <div class="metric-label">Total Feedback</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-value">{stats['approval_rate']:.1%} {approval_trend}</div>
            <div class="metric-label">Approval Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🧠</div>
            <div class="metric-value">{stats['avg_confidence']:.3f} {confidence_trend}</div>
            <div class="metric-label">Avg Confidence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-value">{st.session_state.agent.learning_rate:.2f}</div>
            <div class="metric-label">Learning Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<h2 class="section-header">📈 Data Visualizations</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Action distribution with enhanced styling
        if stats['top_actions']:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🎯 Action Distribution</div>', unsafe_allow_html=True)
            
            actions_df = pd.DataFrame(stats['top_actions'], columns=['Action', 'Count'])
            fig = px.bar(
                actions_df, 
                x='Action', 
                y='Count',
                color='Count',
                color_continuous_scale='viridis',
                title=''
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Top senders with enhanced styling
        if stats['top_senders']:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">👥 Top Senders</div>', unsafe_allow_html=True)
            
            senders_df = pd.DataFrame(stats['top_senders'], columns=['Sender', 'Count'])
            fig = px.pie(
                senders_df, 
                values='Count', 
                names='Sender',
                title='',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Performance Section
    if stats['recent_performance']:
        st.markdown('<h2 class="section-header">📈 Performance Trends</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="performance-card">', unsafe_allow_html=True)
        st.markdown('<div class="performance-title">🚀 Recent Performance Analytics</div>', unsafe_allow_html=True)
        
        perf_df = pd.DataFrame(stats['recent_performance'])
        perf_df['timestamp'] = pd.to_datetime(perf_df['timestamp'])
        
        fig = go.Figure()
        
        # Reward line
        fig.add_trace(go.Scatter(
            x=perf_df['timestamp'], 
            y=perf_df['reward'], 
            mode='lines+markers', 
            name='🎯 Reward',
            line=dict(color='#00d4aa', width=3),
            marker=dict(size=8, color='#00d4aa')
        ))
        
        # Confidence line
        fig.add_trace(go.Scatter(
            x=perf_df['timestamp'], 
            y=perf_df['confidence'], 
            mode='lines+markers', 
            name='🧠 Confidence', 
            yaxis='y2',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#667eea')
        ))
        
        fig.update_layout(
            title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis=dict(
                title='Time',
                gridcolor='rgba(255,255,255,0.1)',
                titlefont=dict(color='white')
            ),
            yaxis=dict(
                title='Reward',
                gridcolor='rgba(255,255,255,0.1)',
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            yaxis2=dict(
                title='Confidence',
                overlaying='y', 
                side='right',
                gridcolor='rgba(255,255,255,0.1)',
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            legend=dict(
                font=dict(color='white'),
                bgcolor='rgba(0,0,0,0.3)',
                bordercolor='rgba(255,255,255,0.2)'
            ),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_stealth_logs():
    """Show stealth logs with embedded data"""
    st.markdown('<h1 class="dashboard-header">🕵️ Stealth Intelligence Logs</h1>', unsafe_allow_html=True)
    
    if not st.session_state.stealth_logs:
        st.markdown("""
        <div class="no-data-card">
            <div class="no-data-icon">🕵️</div>
            <div class="no-data-text">No stealth logs available yet.<br>Start analyzing emails to see hidden intelligence data!</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown('<h2 class="section-header">🔍 Recent Stealth Operations</h2>', unsafe_allow_html=True)
    
    # Show recent logs with enhanced styling
    for i, log in enumerate(reversed(st.session_state.stealth_logs[-10:])):  # Show last 10
        with st.expander(f"🔐 {log['subject']} - {log['emoji_trigger']}", expanded=False):
            st.markdown(f"""
            <div class="email-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="margin: 0;">📧 {log['subject']}</h4>
                    <span class="action-badge">{log['emoji_trigger']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="sender-info">
                    <strong>👤 Sender:</strong> {log['sender']}<br>
                    <strong>🎯 Action:</strong> {log['predicted_action']}<br>
                    <strong>🧠 Confidence:</strong> {log['confidence']:.3f}<br>
                    <strong>💭 Explanation:</strong> {log['explanation']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Decode stealth data
                decoded = st.session_state.steganography.decode_stealth_data(log)
                
                if 'error' not in decoded:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%); 
                                border-radius: 15px; padding: 1rem; color: white; margin-bottom: 1rem;">
                        <strong>✅ Stealth Data Decoded Successfully!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    st.json(decoded['extracted_data'])
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); 
                                border-radius: 15px; padding: 1rem; color: white; margin-bottom: 1rem;">
                        <strong>❌ Decoding Error:</strong> {decoded['error']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 15px; padding: 1rem; color: white;">
                    <strong>🎭 Emoji Trigger:</strong> {log['emoji_trigger']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_feedback_history():
    """Show detailed feedback history"""
    st.markdown('<h1 class="dashboard-header">📝 Learning History</h1>', unsafe_allow_html=True)
    
    if not st.session_state.feedback_history:
        st.markdown("""
        <div class="no-data-card">
            <div class="no-data-icon">📝</div>
            <div class="no-data-text">No feedback history available yet.<br>Start providing feedback to see your learning journey!</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown('<h2 class="section-header">🔍 Feedback Analytics</h2>', unsafe_allow_html=True)
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(st.session_state.feedback_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_feedback = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{total_feedback}</div>
            <div class="metric-label">Total Feedback</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        approvals = len(df[df['user_feedback'] == 'approve'])
        approval_rate = (approvals / total_feedback * 100) if total_feedback > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-value">{approval_rate:.1f}%</div>
            <div class="metric-label">Approval Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_senders = df['sender'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{unique_senders}</div>
            <div class="metric-label">Unique Senders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_reward = df['reward'].mean() if 'reward' in df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-value">{avg_reward:.2f}</div>
            <div class="metric-label">Avg Reward</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔍 Filter & Explore</h2>', unsafe_allow_html=True)
    
    # Filter options with enhanced styling
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🎛️ Filter Options</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        feedback_filter = st.selectbox(
            "Filter by feedback type:", 
            ['All', 'approve', 'reject'],
            help="Choose to filter by approval or rejection feedback"
        )
    
    with col2:
        sender_filter = st.selectbox(
            "Filter by sender:", 
            ['All'] + list(df['sender'].unique()),
            help="Choose to filter by specific email senders"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    if feedback_filter != 'All':
        filtered_df = filtered_df[filtered_df['user_feedback'] == feedback_filter]
    if sender_filter != 'All':
        filtered_df = filtered_df[filtered_df['sender'] == sender_filter]
    
    # Display filtered data with enhanced styling
    st.markdown('<h2 class="section-header">📋 Detailed Records</h2>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        # Style the dataframe
        st.markdown("""
        <style>
        .dataframe {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 1rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display with custom styling
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "timestamp": st.column_config.DatetimeColumn("🕒 Timestamp"),
                "sender": st.column_config.TextColumn("👤 Sender"),
                "subject": st.column_config.TextColumn("📧 Subject"),
                "predicted_action": st.column_config.TextColumn("🎯 Predicted Action"),
                "user_feedback": st.column_config.SelectboxColumn("✅ User Feedback", options=['approve', 'reject']),
                "reward": st.column_config.NumberColumn("🎯 Reward", format="%.2f")
            }
        )
        
        # Show summary of filtered data
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; padding: 1rem; color: white; margin-top: 1rem;">
            <strong>📊 Showing {len(filtered_df)} records</strong> 
            {f"for {feedback_filter} feedback" if feedback_filter != 'All' else ''}
            {f"from {sender_filter}" if sender_filter != 'All' else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="no-data-card">
            <div class="no-data-icon">🔍</div>
            <div class="no-data-text">No records match your current filters.<br>Try adjusting your filter criteria.</div>
        </div>
        """, unsafe_allow_html=True)

# Navigation
st.sidebar.divider()
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Inbox", "📊 Dashboard", "🕵️ Stealth Logs", "📝 Feedback History"]
)

if page == "🏠 Inbox":
    main()
elif page == "📊 Dashboard":
    show_dashboard()
elif page == "🕵️ Stealth Logs":
    show_stealth_logs()
elif page == "📝 Feedback History":
    show_feedback_history()

# Footer
st.sidebar.divider()
st.sidebar.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    🧠 Daily Cognitive Agent<br>
    Powered by Reinforcement Learning
</div>
""", unsafe_allow_html=True)