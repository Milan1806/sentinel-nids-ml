import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import time
import altair as alt

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sentinel-NIDS Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS & STYLING ---
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1, h2, h3 {
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SETUP & LOADING ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(project_root)

@st.cache_resource
def load_resources():
    try:
        model_path = os.path.join(project_root, "models/rf_model.pkl")
        if not os.path.exists(model_path): return None, None
        model = joblib.load(model_path)
        encoders = {}
        for col in ['protocol_type', 'service', 'flag']:
            encoders[col] = joblib.load(os.path.join(project_root, f"models/{col}_encoder.pkl"))
        return model, encoders
    except: return None, None

model, encoders = load_resources()

# --- 4. SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Threat_Score', 'Status', 'Protocol', 'Bytes'])
if 'last_risk' not in st.session_state:
    st.session_state.last_risk = 0.0

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/924/924915.png", width=50)
    st.title("Sentinel Control")
    st.caption("v1.0")
    st.divider()

    b1, b2 = st.columns(2)
    with b1:
        if st.button("😇 Normal", use_container_width=True):
            st.session_state.update({
                'duration': np.random.randint(0,20), 'src_bytes': np.random.randint(200,2000),
                'dst_bytes': np.random.randint(200,50000), 'serror_rate': 0.0, 'count': np.random.randint(1,10),
                'protocol': "http", 'flag': "SF"
            })
    with b2:
        if st.button("😈 Attack", use_container_width=True):
            st.session_state.update({
                'duration': 0, 'src_bytes': 0, 'dst_bytes': 0, 'serror_rate': 1.0,
                'count': np.random.randint(250,511), 'protocol': "tcp", 'flag': "S0"
            })

    st.subheader("Manual Inspection")
    duration = st.number_input("Duration", value=st.session_state.get('duration', 0))
    
    p_idx = ["tcp","udp","icmp","http"].index(st.session_state.get('protocol', "tcp")) if st.session_state.get('protocol') in ["tcp","udp","icmp","http"] else 0
    protocol = st.selectbox("Protocol", ["tcp","udp","icmp","http"], index=p_idx)
    
    f_idx = ["SF","S0","REJ","RSTR"].index(st.session_state.get('flag', "SF")) if st.session_state.get('flag') in ["SF","S0","REJ","RSTR"] else 0
    flag = st.selectbox("Flag", ["SF","S0","REJ","RSTR"], index=f_idx)
    
    src_bytes = st.number_input("Source Bytes", value=st.session_state.get('src_bytes', 491))
    dst_bytes = st.number_input("Destination Bytes", value=st.session_state.get('dst_bytes', 0))
    count = st.slider("Traffic Count", 0, 511, value=st.session_state.get('count', 2))
    serror_rate = st.slider("SYN Error Rate", 0.0, 1.0, value=st.session_state.get('serror_rate', 0.0))

    st.markdown("### ")
    scan = st.button("🔍 SCAN PACKET", type="primary", use_container_width=True)

# --- 6. METRIC CARDS ---
if not model:
    st.error("⚠️ Model missing. Run training script.")
    st.stop()

total_scans = len(st.session_state.history)
malicious = len(st.session_state.history[st.session_state.history['Status'] == 'MALICIOUS'])
risk_score = st.session_state.last_risk * 100

if risk_score > 50:
    risk_color = "#FF4B4B" # Red
    risk_label = "CRITICAL"
else:
    risk_color = "#00CC96" # Green
    risk_label = "SAFE"

def card(title, value, sub_text, sub_color):
    st.markdown(f"""
    <div style="
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
        margin-bottom: 10px;
    ">
        <p style="color: #b0b0b0; margin: 0; font-size: 14px; font-weight: 500;">{title}</p>
        <h2 style="color: white; margin: 8px 0; font-size: 32px; font-weight: 700;">{value}</h2>
        <div style="display: inline-block; background-color: {sub_color}20; padding: 4px 8px; border-radius: 4px;">
            <span style="color: {sub_color}; font-size: 12px; font-weight: bold;">{sub_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: card("Total Scans", f"{total_scans}", "LIVE", "#00CC96")
with c2: card("Threats Blocked", f"{malicious}", "LIFETIME", "#FF4B4B")
with c3: card("Last Packet Risk", f"{risk_score:.1f}%", risk_label, risk_color)
with c4: card("Protocol", protocol.upper(), "ACTIVE", "#3399FF")

st.divider()

# --- 7. LOGIC ---
if scan:
    input_data = np.zeros(41)
    input_data[0] = duration
    input_data[4] = src_bytes
    input_data[5] = dst_bytes
    input_data[22] = count
    input_data[24] = serror_rate
    
    if serror_rate > 0.5:
        input_data[25] = serror_rate
        input_data[29] = 1.0
        input_data[32] = 255
    else:
        input_data[28] = 1.0

    def safe_transform(enc, val): return enc.transform([val])[0] if val in enc.classes_ else -1
    input_data[1] = safe_transform(encoders['protocol_type'], protocol)
    input_data[2] = safe_transform(encoders['service'], 'private') 
    input_data[3] = safe_transform(encoders['flag'], flag)
    
    pred = model.predict([input_data])[0]
    prob = model.predict_proba([input_data])[0][1]
    st.session_state.last_risk = prob
    
    new_row = pd.DataFrame({
        'Time': [time.strftime("%H:%M:%S")], 'Threat_Score': [prob],
        'Status': ["MALICIOUS" if pred==1 else "NORMAL"],
        'Protocol': [protocol], 'Bytes': [src_bytes + dst_bytes]
    })
    st.session_state.history = pd.concat([new_row, st.session_state.history], ignore_index=True)
    st.rerun()

# --- 8. VISUALS ---
if not st.session_state.history.empty:
    c1, c2 = st.columns([1,1])
    
    with c1:
        st.subheader("🚦 Traffic Distribution")
        df = st.session_state.history['Status'].value_counts().reset_index()
        df.columns = ['Status', 'Count']
        base = alt.Chart(df).encode(theta=alt.Theta("Count", stack=True))
        pie = base.mark_arc(outerRadius=100, innerRadius=60).encode(
            color=alt.Color("Status", scale=alt.Scale(domain=['MALICIOUS', 'NORMAL'], range=['#FF4B4B', '#00CC96'])),
            tooltip=["Status", "Count"]
        )
        st.altair_chart(pie, use_container_width=True)

    with c2:
        st.subheader("📡 Protocol Usage")
        df_p = st.session_state.history['Protocol'].value_counts().reset_index()
        df_p.columns = ['Protocol', 'Count']
        bar = alt.Chart(df_p).mark_bar().encode(
            x='Protocol', y='Count',
            color=alt.Color('Protocol', scale=alt.Scale(scheme='tableau10')),
            tooltip=['Protocol', 'Count']
        )
        st.altair_chart(bar, use_container_width=True)

    st.subheader("📈 Risk Timeline")
    df_time = st.session_state.history.head(50).reset_index()
    
    # --- FIXED: Use offset and color keywords explicitly ---
    area = alt.Chart(df_time).mark_area(
        line={'color':'#FF4B4B'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(offset=0, color='#FF4B4B'), alt.GradientStop(offset=1, color='rgba(255, 75, 75, 0.1)')],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('index', title='Packets', axis=None),
        y='Threat_Score'
    ).properties(height=250)
    st.altair_chart(area, use_container_width=True)

    st.subheader("📜 Live Packet Inspector")
    st.dataframe(
        st.session_state.history,
        column_order=("Time", "Status", "Threat_Score", "Protocol", "Bytes"),
        column_config={
            "Threat_Score": st.column_config.ProgressColumn("Risk Level", format="%.2f", min_value=0, max_value=1),
            "Bytes": st.column_config.NumberColumn("Size", format="%d B"),
        },
        use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ No traffic data. Click 'Normal' or 'Attack' in the sidebar to simulate network flow.")
    
    st.markdown("""
    ### 📖 User Guide
    **1. 😇 Normal Traffic (Green Button)**
    * Simulates legitimate user activity (Standard HTTP/TCP requests).
    * **Expected Result:** Low risk score, Green "SAFE" status.
    
    **2. 😈 Attack Traffic (Red Button)**
    * Simulates a **Neptune DoS Attack** (SYN Flood).
    * **Expected Result:** High risk score (>90%), Red "CRITICAL" alert.
    """)