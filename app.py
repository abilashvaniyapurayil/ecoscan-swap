import streamlit as st
from PIL import Image
import pandas as pd
import json
import os
from fpdf import FPDF

# 1. PAGE CONFIG
st.set_page_config(page_title="EcoScan Pro: Salmiya", page_icon="🌱", layout="wide")

# --- Database & Centers ---
DB_FILE = "items_db.json"
RECYCLING_CENTERS = [
    {"name": "Salmiya Block 4 Drop-off", "user": "OFFICIAL CENTER", "lat": 29.3325, "lon": 48.0680, "eco": 0, "cat": "Recycling"},
    {"name": "Salmiya Co-op Collection", "user": "OFFICIAL CENTER", "lat": 29.3415, "lon": 48.0730, "eco": 0, "cat": "Recycling"}
]

def load_data():
    user_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: user_data = json.load(f)
    return user_data + RECYCLING_CENTERS

def save_item(name, user, lat, lon, eco, cat):
    current_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: current_data = json.load(f)
    current_data.append({"name": name, "user": user, "lat": lat, "lon": lon, "eco": eco, "cat": cat})
    with open(DB_FILE, "w") as f: json.dump(current_data, f)

# --- Calculations ---
full_data = load_data()
user_items = [d for d in full_data if d['user'] != "OFFICIAL CENTER"]
total_saved = 5120 + sum([int(str(d['eco']).replace('kg','')) for d in user_items if 'eco' in d])

# --- Sidebar ---
st.sidebar.title("🌍 Salmiya Impact")
st.sidebar.metric(label="Total CO2 Saved", value=f"{total_saved} kg")

# --- Certificate Function ---
def create_certificate(name, amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 20, "Eco-Warrior Certificate", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 16)
    pdf.cell(200, 10, f"This is to certify that", ln=True, align='C')
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 15, name, ln=True, align='C')
    pdf.set_font("Arial", '', 16)
    pdf.multi_cell(0, 10, f"has successfully prevented {amount}kg of CO2 emissions in Salmiya, Kuwait through the EcoScan & Swap community.", align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- Main App ---
st.title("🌱 EcoScan & Swap")
t1, t2, t3, t4 = st.tabs(["📤 Scan", "📍 Map", "📱 Feed", "🏆 Rewards"])

with t1:
    st.subheader("Post an Item")
    cat_list = ["Furniture", "Electronics", "Clothes", "Sports"]
    item_cat = st.selectbox("Category", cat_list)
    up = st.file_uploader("Scan item photo", type=["jpg", "png", "jpeg"])
    if up:
        if st.button("Confirm & Post"):
            save_item(up.name.split('.')[0], "You", 29.33 + (len(user_items)*0.005), 48.07 + (len(user_items)*0.005), "10kg", item_cat)
            st.success("Posted!")
            st.balloons()

with t2:
    st.subheader("Neighborhood Map")
    map_df = pd.DataFrame(full_data)
    map_df['color'] = map_df['user'].apply(lambda x: '#FFFF00' if x == "OFFICIAL CENTER" else ('#00FF00' if x == "You" else '#0000FF'))
    st.map(map_df, latitude='lat', longitude='lon', color='color', zoom=13)

with t3:
    st.subheader("Neighborhood Feed")
    for item in reversed(user_items):
        with st.container(border=True):
            st.write(f"**{item['name']}**")
            st.caption(f"👤 {item['user']} | 🌱 {item['eco']} Saved")

with t4:
    st.subheader("Your Achievements")
    st.write(f"Current Impact: **{total_saved}kg**")
    if total_saved >= 5000:
        st.success("🎉 You have unlocked the Eco-Warrior Status!")
        user_name = st.text_input("Enter your name for the certificate:")
        if user_name:
            pdf_data = create_certificate(user_name, total_saved)
            st.download_button(label="📥 Download Certificate", data=pdf_data, file_name="eco_warrior.pdf", mime="application/pdf")
    else:
        st.info("Keep swapping! You need 5,000kg to unlock your certificate.")
