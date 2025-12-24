import streamlit as st
import pandas as pd
import json
import os
import random
import base64
from datetime import datetime
from PIL import Image
import io

# --- 1. BRANDED PAGE SETUP ---
st.set_page_config(
    page_title="EcoScan Kuwait | Professional Portal",
    page_icon="🇰🇼",
    layout="wide"
)

# --- 2. DATA MANAGEMENT ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
FEEDBACK_DB = "feedback_db.json"
FOUNDER_IMAGE = "founder.jpeg"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Helper function to convert images to strings for JSON storage
def image_to_base64(uploaded_file):
    if uploaded_file is not None:
        return base64.b64encode(uploaded_file.getvalue()).decode()
    return None

# --- 3. SESSION LOGIC ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 4. PROFESSIONAL SIDEBAR ---
with st.sidebar:
    st.title("🇰🇼 EcoScan")
    st.caption("Kuwait's National Swap Network")
    
    # Founder Section
    with st.expander("👤 Founder's Message", expanded=False):
        if os.path.exists(FOUNDER_IMAGE):
            st.image(FOUNDER_IMAGE, use_container_width=True)
        st.info("**Abilash Vani**\nHelping Kuwait reach zero-waste goals through community action.")
        st.link_button("💬 Support WhatsApp", "https://wa.me/96512345678")

    st.divider()

    if st.session_state.user:
        # Display User Metrics
        users = load_data(USER_DB)
        db_user = next((u for u in users if u['phone'] == st.session_state.user['phone']), st.session_state.user)
        st.metric("🌱 Eco-Points", f"{db_user.get('points', 0)} PTS")
        st.write(f"Verified: **{db_user['name']}**")
        st.caption(f"📍 {db_user['area']}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        # Professional Login/Signup Forms
        if st.session_state.view == "login":
            st.subheader("Login")
            phone = st.text_input("Mobile")
            pw = st.text_input("Password", type="password")
            if st.button("Access Portal", type="primary", use_container_width=True):
                users = load_data(USER_DB)
                u = next((u for u in users if u['phone'] == phone and u['password'] == pw), None)
                if u: 
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Access Denied")
            if st.button("Create Account"): st.session_state.view = "signup"; st.rerun()
        else:
            st.subheader("Register")
            s_name = st.text_input("Full Name")
            s_phone = st.text_input("Mobile Number")
            s_area = st.selectbox("Area", ["Asimah", "Hawalli", "Farwaniya", "Ahmadi", "Jahra", "Mubarak"])
            s_pw = st.text_input("Password", type="password")
            if st.button("Join Movement", type="primary"):
                users = load_data(USER_DB)
                users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pw, "points": 10})
                save_data(USER_DB, users)
                st.session_state.view = "login"
                st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user:
    # Header Banner
    st.markdown("""
        <div style="background-color:#2E7D32;padding:25px;border-radius:15px;color:white;text-align:center">
            <h1 style="color:white;margin:0">Sustainable Kuwait Portal</h1>
            <p style="margin:0">Every swap reduces Kuwait's landfill waste.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs(["📤 Post Item", "📱 Search Feed", "🏆 Leaderboard", "📩 Suggestions"])

    with tab1:
        st.subheader("List a New Swap")
        with st.form("professional_post", clear_on_submit=True):
            col1, col2 = st.columns(2)
            item_name = col1.text_input("Item Name")
            item_cat = col2.selectbox("Category", ["Electronics", "Furniture", "Books", "Clothing", "Other"])
            item_desc = st.text_area("Describe the condition and pickup details")
            item_img = st.file_uploader("Upload Item Photo (Optional)", type=['jpg', 'png', 'jpeg'])
            
            if st.form_submit_button("Publish to Marketplace (+10 Points)"):
                if item_name:
                    items = load_data(ITEM_DB)
                    img_data = image_to_base64(item_img)
                    items.append({
                        "id": str(datetime.now().timestamp()),
                        "name": item_name, "desc": item_desc, "cat": item_cat,
                        "user": st.session_state.user['name'], "area": st.session_state.user['area'],
                        "image": img_data, "date": datetime.now().strftime("%Y-%m-%d")
                    })
                    save_data(ITEM_DB, items)
                    # Reward Points
                    users = load_data(USER_DB)
                    for u in users:
                        if u['phone'] == st.session_state.user['phone']: u['points'] = u.get('points', 0) + 10
                    save_data(USER_DB, users)
                    st.success("Your item is now live!")
                    st.balloons()
                    st.rerun()

    with tab2:
        st.subheader("Available Community Swaps")
        search = st.text_input("🔍 Search by name, category, or area...")
        all_items = load_data(ITEM_DB)
        filtered = [i for i in all_items if search.lower() in i['name'].lower() or search.lower() in i['cat'].lower() or search.lower() in i['area'].lower()]
        
        if not filtered:
            st.info("No items found matching your search.")
        else:
            for i in reversed(filtered):
                with st.container(border=True):
                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        if i.get("image"):
                            st.image(base64.b64decode(i["image"]), use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300?text=No+Image", use_container_width=True)
                    with col_info:
                        st.markdown(f"### {i['name']}")
                        st.markdown(f"**Category:** {i['cat']} | **Location:** {i['area']}")
                        st.write(i['desc'])
                        st.caption(f"Posted by {i['user']} on {i.get('date', 'Unknown')}")
                        st.button("Request Item", key=i['id'])

    with tab3:
        st.subheader("🏆 National Eco-Warriors")
        all_users = load_data(USER_DB)
        if all_users:
            df = pd.DataFrame(all_users)[['name', 'area', 'points']].sort_values('points', ascending=
