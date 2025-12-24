import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="wide")

# --- 2. PRIVACY POLICY CONTENT (App Store Compliant) ---
PRIVACY_POLICY = """
### 🛡️ Privacy Policy for EcoScan Kuwait
**Last Updated: December 2025**

To comply with App Store and Google Play requirements, we provide full transparency:

1. **Information Collection**: We collect your Name, Email, Phone Number, and Governorate to facilitate community swaps.
2. **Data Usage**: Your data is used only to manage your account and send notifications. We do NOT sell your data to third parties.
3. **Data Security**: We use secure storage protocols to protect your personal identifiers.
4. **User Rights**: You may request the deletion of your account and all associated data at any time by contacting the Founder via the Support tab.
5. **Location Transparency**: We use your 'Governorate' selection only to show you relevant local items.
"""

# --- 3. DATABASE FUNCTIONS ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try: return json.load(f)
            except: return []
    return []

# --- 4. MAIN INTERFACE ---
if st.session_state.get("user"):
    st.title("🌱 EcoScan Kuwait")
    
    # We add the new "Legal & Privacy" tab here
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Post", "📱 Feed", "🏆 Rankings", "📩 Support", "📜 Legal"
    ])

    with tab1:
        st.subheader("Add Listing")
        # (Your existing post logic here)

    with tab2:
        st.subheader("Community Swaps")
        # (Your existing feed logic here)

    with tab3:
        st.subheader("Leaderboard")
        # (Your existing ranking logic here)

    with tab4:
        st.subheader("Contact Support")
        # (Your existing support logic here)

    with tab5:
        st.info("This section is required for publishing on mobile app stores.")
        st.markdown(PRIVACY_POLICY)
        if st.button("Download Policy as PDF"):
            st.write("Generating document...") # You can use fpdf here later if needed

else:
    # Login/Signup Logic
    st.info("### Welcome to EcoScan Kuwait\nPlease login to join our green community.")
    with st.expander("Read Privacy Policy before joining"):
        st.markdown(PRIVACY_POLICY)
