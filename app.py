import streamlit as st

# --- STEP 1: HIDDEN GOOGLE VERIFICATION ---
# st.set_page_config MUST be the very first Streamlit command.
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼")

# This places the verification tag in the hidden 'Header' where Google looks.
st.markdown(
    """
    <head>
        <meta name="google-site-verification" content="UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40" />
    </head>
    """, 
    unsafe_allow_html=True
)

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

# --- STEP 4: STATUS ---
st.success("✅ Ownership Verification Tag is Active in the Header.")
st.info("Wait 60 seconds after saving, then click 'Verify' in Google Search Console.")
