import streamlit as st

# --- STEP 1: GOOGLE VERIFICATION (Must be at the very top) ---
# This is the meta tag Google is looking for. 
# It is now public and outside any login checks.
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- STEP 2: APP STYLE ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼")

st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .founder-card { 
        background-color: #ffffff; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- STEP 3: PUBLIC CONTENT (Founder Vision) ---
# This is always visible to everyone (and Google's bot).
st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Community Sustainability Portal</p></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="founder-card">
    <h3>Founder's Vision</h3>
    <p>"EcoScan Kuwait is a movement to protect our environment by sharing resources. 
    Every swap reduces landfill waste in our beautiful country."</p>
    <p><b>— Founder: Abhilash Babu</b></p>
</div>
""", unsafe_allow_html=True)

st.info("The community marketplace is currently under maintenance. Google Verification in progress.")
