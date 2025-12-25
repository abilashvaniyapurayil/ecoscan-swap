import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. CONFIG & APP STORE META ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🌱", layout="centered")

# Hidden metadata for search engines and app wrappers
st.markdown("""
    <head>
        <meta name="description" content="EcoScan Kuwait - The National Community Swap Platform.">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ENGINE ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- 3. STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white; padding: 20px;
        border-radius: 15px; text-align: center; margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION LOGIC ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 5. APP CONTENT ---
if st.session_state.user:
    # LOGGED IN VIEW
    is_admin = st.session_state.user.get("role") == "admin"
    st.markdown(f'<div class="main-banner"><h1>EcoScan Kuwait</h1><p>Welcome, {st.session_state.user["name"]}</p></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📤 Post Item", "📱 Community Feed", "⚖️ Legal"])

    with tabs[0]:
        st.subheader("What are you swapping today?")
        with st.form("post_form", clear_on_submit=True):
            i_name = st.text_input("Item Name")
            i_cat = st.selectbox("Category", ["Furniture", "Electronics", "Clothing", "Books", "Other"])
            if st.form_submit_button("Post to Marketplace"):
                if i_name:
                    items = load_data(ITEM_DB)
                    items.append({
                        "id": str(datetime.now().timestamp()), 
                        "name": i_name, "cat": i_cat, 
                        "user": st.session_state.user['name'], 
                        "area": st.session_state.user['area']
                    })
                    save_data(ITEM_DB, items)
                    st.success("Item is now live!")

    with tabs[1]:
        st.subheader("Available in Kuwait")
        items = load_data(ITEM_DB)
        if not items: st.info("No items posted yet.")
        for i in reversed(items):
            with st.container(border=True):
                st.write(f"### {i['name']}")
                st.caption(f"📍 {i['area']} | Category: {i['cat']} | Posted by: {i['user']}")
                if is_admin:
                    if st.button(f"Remove Item {i['id'][:5]}", key=i['id']):
                        items = [item for item in items if item['id'] != i['id']]
                        save_data(ITEM_DB, items)
                        st.rerun()

    with tabs[2]:
        st.subheader("⚖️ Privacy & Support")
        st.write("EcoScan Kuwait respects your data. We only collect your phone number for secure verification.")
        st.link_button("Contact Support", "https://wa.me/96590000000") # Replace with your number
        if st.button("Log Out"):
            st.session_state.user = None
            st.rerun()

else:
    # LOGIN / SIGNUP VIEW
    st.markdown('<div class="main-banner"><h1>🌱 EcoScan Kuwait</h1><p>The Circular Economy</p></div>', unsafe_allow_html=True)
    
    if st.session_state.view == "login":
        st.subheader("Login")
        u_phone = st.text_input("Phone Number")
        u_pw = st.text_input("Password", type="password")
        if st.button("Sign In", type="primary"):
            # Admin Backdoor
            if u_phone == "90000000" and u_pw == "founder2025":
                st.session_state.user = {"name": "Founder", "phone": "90000000", "area": "Kuwait City", "role": "admin"}
                st.rerun()
            # Standard User Check
            users = load_data(USER_DB)
            u = next((u for u in users if u['phone'] == u_phone and u['password'] == u_pw), None)
            if u: 
                st.session_state.user = u
                st.rerun()
            else: st.error("Incorrect details. Please try again.")
        if st.button("New here? Create an Account"):
            st.session_state.view = "signup"
            st.rerun()
    
    else:
        st.subheader("Create Account")
        s_name = st.text_input("Full Name")
        s_phone = st.text_input("Phone Number")
        s_area = st.selectbox("Governorate", ["Asimah", "Hawalli", "Farwaniya", "Ahmadi", "Jahra", "Mubarak"])
        s_pw = st.text_input("Create Password", type="password")
        if st.button("Join EcoScan"):
            if s_name and s_phone and s_pw:
                users = load_data(USER_DB)
                users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pw, "role": "user"})
                save_data(USER_DB, users)
                st.success("Welcome! Now please login.")
                st.session_state.view = "login"
                st.rerun()
            else: st.warning("Please fill all fields.")
