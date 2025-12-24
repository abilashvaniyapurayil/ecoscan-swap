import streamlit as st
import pandas as pd
import json
import os
from fpdf import FPDF

# 1. PAGE CONFIG
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="wide")

USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
# CHANGED TO MATCH YOUR GITHUB FILENAME
FOUNDER_IMAGE = "founder.jpeg" 
KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]

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

# --- SIDEBAR ---
with st.sidebar:
    st.header("🇰🇼 EcoScan Kuwait")
    
    # --- FOUNDER'S CORNER ---
    st.subheader("👤 Founder's Corner")
    if os.path.exists(FOUNDER_IMAGE):
        st.image(FOUNDER_IMAGE, use_container_width=True)
        st.info("**Abilash's Message:** Welcome to our national swap community! Let's build a greener Kuwait together.")
    else:
        st.warning(f"Searching for '{FOUNDER_IMAGE}'... Please ensure the filename on GitHub matches line 12 of your code exactly.")
    
    st.divider()

    # --- ACCOUNT SYSTEM ---
    if st.session_state.user is None:
        if st.session_state.view == "login":
            st.markdown("### Login")
            l_phone = st.text_input("Phone Number")
            l_pass = st.text_input("Password", type="password")
            if st.button("Log In", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                u = next((u for u in users if u['phone'] == l_phone and u['password'] == l_pass), None)
                if u:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Invalid Login")
            
            if st.button("No account? Click to Sign Up", use_container_width=True):
                st.session_state.view = "signup"
                st.rerun()

        elif st.session_state.view == "signup":
            st.markdown("### 📝 Create New Account")
            s_name = st.text_input("Full Name")
            s_phone = st.text_input("Mobile Number")
            s_area = st.selectbox("Select Governorate", KUWAIT_AREAS)
            s_pass = st.text_input("Create Password", type="password")
            
            if st.button("Register Now", type="primary", use_container_width=True):
                if s_name and s_phone and s_pass:
                    users = load_json(USER_DB)
                    users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pass})
                    save_json(USER_DB, users)
                    st.success("Account Created! Please Login.")
                    st.session_state.view = "login"
                    st.rerun()
                else:
                    st.error("Please fill all fields")
            
            if st.button("Back to Login"):
                st.session_state.view = "login"
                st.rerun()
    else:
        st.success(f"Hello, {st.session_state.user['name']}!")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

# --- MAIN PAGE ---
st.title("🌱 EcoScan Kuwait")
if st.session_state.user:
    st.write(f"Welcome to the portal, **{st.session_state.user['name']}**. You are registered in **{st.session_state.user['area']}**.")
else:
    st.info("### Please use the sidebar to Login or Sign Up.")
    st.image("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&q=80&w=1000", caption="Join the movement.")
