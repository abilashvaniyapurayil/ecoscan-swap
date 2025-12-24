import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="wide")

# --- Database Setup ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
FOUNDER_IMAGE = "founder.jpeg" 
KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]
CATEGORIES = ["Furniture", "Electronics", "Books", "Clothes", "Appliances", "Other"]

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f: 
            try: return json.load(f)
            except: return []
    return []

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

# Initialize Session States
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- SIDEBAR: Founder & Account ---
with st.sidebar:
    st.header("🇰🇼 EcoScan Kuwait")
    
    # Founder's Corner (Verified working from your screenshots)
    st.subheader("👤 Founder's Corner")
    if os.path.exists(FOUNDER_IMAGE):
        st.image(FOUNDER_IMAGE, use_container_width=True)
        st.info("**Abilash's Message:** Let's build a greener Kuwait! Swap items to reduce waste in our community.")
        # WhatsApp Link
        st.link_button("💬 Chat with Founder", "https://wa.me/96512345678", use_container_width=True)
    
    st.divider()

    # Account Management
    if st.session_state.user is None:
        if st.session_state.view == "login":
            st.markdown("### 🔑 Login")
            l_phone = st.text_input("Phone Number")
            l_pass = st.text_input("Password", type="password")
            if st.button("Log In", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                u = next((u for u in users if u['phone'] == l_phone and u['password'] == l_pass), None)
                if u:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Check number/password")
            if st.button("New? Sign Up"): st.session_state.view = "signup"; st.rerun()

        elif st.session_state.view == "signup":
            st.markdown("### 📝 Register")
            s_name = st.text_input("Full Name")
            s_phone = st.text_input("Mobile")
            s_area = st.selectbox("Governorate", KUWAIT_AREAS)
            s_pass = st.text_input("Password", type="password")
            if st.button("Join Now", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pass})
                save_json(USER_DB, users)
                st.success("Created! Please Login.")
                st.session_state.view = "login"; st.rerun()
            if st.button("Back"): st.session_state.view = "login"; st.rerun()
    else:
        st.success(f"User: {st.session_state.user['name']}")
        st.caption(f"📍 {st.session_state.user['area']}")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None; st.rerun()

# --- MAIN PAGE CONTENT ---
st.title("🌱 EcoScan Kuwait: Swap Portal")

if st.session_state.user:
    tab1, tab2 = st.tabs(["📤 Post Item", "📱 Search & Swap Feed"])

    # TAB 1: POSTING
    with tab1:
        st.subheader("List an item for the community")
        c1, c2 = st.columns(2)
        with c1:
            item_name = st.text_input("What are you giving away?")
            item_desc = st.text_area("Item Details (Condition, size, etc.)")
        with c2:
            item_cat = st.selectbox("Category", CATEGORIES)
            item_cond = st.select_slider("Condition", options=["Fair", "Good", "Excellent", "New"])

        if st.button("🚀 Publish Nationally", type="primary"):
            if item_name:
                items = load_json(ITEM_DB)
                items.append({
                    "id": str(datetime.now().timestamp()),
                    "name": item_name, "desc": item_desc, "cat": item_cat, "cond": item_cond,
                    "user": st
