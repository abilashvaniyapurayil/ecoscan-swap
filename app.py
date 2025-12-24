import streamlit as st

# --- STEP 1: GOOGLE ANALYTICS & VERIFICATION (MUST BE FIRST) ---
# This script injects your Analytics ID into the app's head.
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼")

ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XYKY07PYHX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-XYKY07PYHX');
    </script>
    <meta name="google-site-verification" content="UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40" />
"""
st.markdown(ga_code, unsafe_allow_html=True)

# --- STEP 2: PROFESSIONAL STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .vision-card {
        background-color: #ffffff; padding: 25px; border-radius: 15px; 
        border-left: 10px solid #2E7D32; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- STEP 3: YOUR FOUNDER CONTENT ---
st.markdown('<div class="main-banner"><h1>KW EcoScan Kuwait</h1><p>Community Sustainability Portal</p></div>', unsafe_allow_html=True)

st.markdown("""
<div class="vision-card">
    <h2 style="color: #2E7D32;">Our Vision</h2>
    <p style="font-size: 1.2em; font-style: italic;">
        "EcoScan Kuwait is more than an app; it is a movement to protect our environment 
        by sharing resources. Every swap reduces landfill waste in our beautiful country."
    </p>
    <p><b>— Founder: Abhilash Babu</b></p>
</div>
""", unsafe_allow_html=True)

st.divider()
st.success("✅ Google Analytics & Verification Tag are Active.")
st.info("Wait 60 seconds for the cloud to update, then click 'Verify' in Google Search Console.")
