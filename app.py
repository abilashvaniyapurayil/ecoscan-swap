import streamlit as st

# --- STEP 1: PUBLIC GOOGLE VERIFICATION (Must be FIRST) ---
# This remains visible even if the user isn't logged in.
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- STEP 2: APP CONFIG & STYLE ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .stButton>button { border-radius: 20px; width: 100%; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- STEP 3: LOGIN LOGIC ---
# Check if secrets are configured
if "auth" not in st.secrets:
    st.error("⚠️ Configuration missing in Streamlit Cloud Secrets dashboard.")
    st.stop()

if not st.user.is_logged_in:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Join the Sustainability Community</p></div>', unsafe_allow_html=True)
    st.subheader("Sign in to start swapping")
    
    if st.button("Continue with Google", type="primary"):
        st.login() # Triggers Google OAuth using st.secrets
    st.stop()

# --- STEP 4: PROTECTED CONTENT (Only for logged-in users) ---
st.markdown(f'<div class="main-banner"><h1>EcoScan Kuwait</h1><p>Welcome, {st.user.name}!</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📱 Marketplace Feed", "⚙️ Account"])

with tab1:
    st.subheader("Community Listings")
    st.info("No items posted in Kuwait yet. Be the first!")

with tab2:
    st.write(f"Logged in as: **{st.user.email}**")
    if st.button("Log Out"):
        st.logout()
