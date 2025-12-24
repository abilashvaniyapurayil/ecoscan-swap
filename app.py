import streamlit as st
import pandas as pd
import json
import os

# 1. PAGE CONFIG
st.set_page_config(page_title="EcoScan Kuwait Pro", page_icon="🇰🇼", layout="wide")

USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f: return json.load(f)
    return []

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

# --- Session State Management ---
if "user" not in st.session_state:
    st.session_state.user = None
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- Sidebar: Account Center ---
st.sidebar.title("👤 Account Center")

if st.session_state.user is None:
    # 1. Social Login Interface (Visual Only)
    st.sidebar.markdown("### Quick Login")
    st.sidebar.button("Continue with Google 🌐", use_container_width=True)
    st.sidebar.button("Continue with Facebook 🔵", use_container_width=True)
    st.sidebar.divider()

    # 2. Login View
    if st.session_state.view == "login":
        st.sidebar.subheader("Login")
        l_phone = st.sidebar.text_input("Phone Number")
        l_pass = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Log In", type="primary", use_container_width=True):
            users = load_json(USER_DB)
            u = next((u for u in users if u['phone'] == l_phone and u['password'] == l_pass), None)
            if u:
                st.session_state.user = u
                st.rerun()
            else: st.sidebar.error("Invalid credentials")
        
        col1, col2 = st.sidebar.columns(2)
        if col1.button("Sign Up"): st.session_state.view = "signup"; st.rerun()
        if col2.button("Forgot?"): st.session_state.view = "forgot"; st.rerun()

    # 3. Forgot Password View
    elif st.session_state.view == "forgot":
        st.sidebar.subheader("Reset Password")
        f_phone = st.sidebar.text_input("Enter Registered Mobile")
        f_new = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("Update Password"):
            users = load_json(USER_DB)
            found = False
            for u in users:
                if u['phone'] == f_phone:
                    u['password'] = f_new
                    found = True; break
            if found:
                save_json(USER_DB, users)
                st.sidebar.success("Password Updated!")
                st.session_state.view = "login"; st.rerun()
            else: st.sidebar.error("Number not found")
        if st.sidebar.button("Back"): st.session_state.view = "login"; st.rerun()

else:
    # --- LOGGED IN: Edit Profile Section ---
    st.sidebar.success(f"Hello, {st.session_state.user['name']}!")
    
    with st.sidebar.expander("⚙️ Edit My Profile"):
        edit_name = st.text_input("Full Name", value=st.session_state.user['name'])
        edit_area = st.selectbox("My Area", KUWAIT_AREAS, index=KUWAIT_AREAS.index(st.session_state.user.get('area', 'Asimah')))
        edit_phone = st.text_input("Contact Number", value=st.session_state.user['phone'])
        
        if st.button("Save Profile Changes"):
            users = load_json(USER_DB)
            for u in users:
                if u['phone'] == st.session_state.user['phone']:
                    u['name'] = edit_name
                    u['area'] = edit_area
                    u['phone'] = edit_phone
                    st.session_state.user = u # Update current session
                    break
            save_json(USER_DB, users)
            st.toast("Profile updated successfully!")
            st.rerun()

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()

# --- Main App Content ---
st.title("🌱 EcoScan Kuwait")
if st.session_state.user:
    st.write(f"Showing items for your area: **{st.session_state.user['area']}**")
    # (Rest of your tab logic for Map, Feed, etc. goes here)
else:
    st.warning("Please Login or Sign Up to view the community feed.")
