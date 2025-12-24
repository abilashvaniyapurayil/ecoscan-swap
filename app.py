import streamlit as st
from PIL import Image
import pandas as pd
import json
import os
from fpdf import FPDF

# 1. PAGE CONFIG (Updated for Kuwait)
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="wide")

# --- Database & Config ---
DB_FILE = "items_db.json"
# Updated Recycling Centers for different areas in Kuwait
RECYCLING_CENTERS = [
    {"name": "Salmiya Collection Point", "user": "OFFICIAL", "lat": 29.3325, "lon": 48.0680, "cat": "Recycling", "area": "Hawalli"},
    {"name": "Shuwaikh Industrial Center", "user": "OFFICIAL", "lat": 29.3500, "lon": 47.9500, "cat": "Recycling", "area": "Asimah"},
    {"name": "Ahmadi Eco-Hub", "user": "OFFICIAL", "lat": 29.0761, "lon": 48.0838, "cat": "Recycling", "area": "Ahmadi"}
]

KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]

def load_data():
    user_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: user_data = json.load(f)
    if not user_data:
        user_data = [{"name": "Water Cooler", "user": "Zaid", "lat": 29.3759, "lon": 47.9774, "eco": "40kg", "cat": "Electronics", "area": "Asimah"}]
    return user_data + RECYCLING_CENTERS

def save_item(name, user, lat, lon, eco, cat, area):
    current_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: current_data = json.load(f)
    current_data.append({"name": name, "user": user, "lat": lat, "lon": lon, "eco": eco, "cat": cat, "area": area})
    with open(DB_FILE, "w") as f: json.dump(current_data, f)

# --- Logic: Search & Filters ---
full_data = load_data()
user_items = [d for d in full_data if d['user'] != "OFFICIAL"]

st.sidebar.title("🇰🇼 Kuwait Eco-Impact")
search_query = st.sidebar.text_input("🔍 Search items", "").lower()
selected_area = st.sidebar.selectbox("Filter by Governorate:", ["All Kuwait"] + KUWAIT_AREAS)

# Filter Logic
filtered_data = [
    d for d in full_data 
    if (search_query in d['name'].lower()) and 
    (selected_area == "All Kuwait" or d.get('area') == selected_area)
]

# --- Main App ---
st.title("🌱 EcoScan & Swap: Kuwait")
t1, t2, t3, t4 = st.tabs(["📤 Post Item", "📍 Kuwait Map", "📱 National Feed", "🏆 Rankings"])

with t1:
    st.subheader("Contribute to Kuwait's Green Future")
    col1, col2 = st.columns(2)
    with col1:
        item_cat = st.selectbox("Category", ["Furniture", "Electronics", "Clothes", "Sports"])
        user_area = st.selectbox("Your Location", KUWAIT_AREAS)
    with col2:
        up = st.file_uploader("Scan item photo", type=["jpg", "png", "jpeg"])
    
    if up and st.button("Post to Kuwait Feed"):
        # Map centering coordinates for the selected area (simplified for demo)
        area_coords = {"Asimah": (29.37, 47.97), "Hawalli": (29.33, 48.06), "Ahmadi": (29.07, 48.08)}
        lat, lon = area_coords.get(user_area, (29.31, 47.48))
        save_item(up.name.split('.')[0], "You", lat, lon, "10kg", item_cat, user_area)
        st.success(f"Success! Your item is live in {user_area}.")
        st.balloons()

with t2:
    st.subheader(f"Eco-Map: {selected_area}")
    if filtered_data:
        map_df = pd.DataFrame(filtered_data)
        map_df['color'] = map_df['user'].apply(lambda x: '#FFFF00' if x == "OFFICIAL" else ('#00FF00' if x == "You" else '#0000FF'))
        # Zoom 10 covers the main populated areas of Kuwait
        st.map(map_df, latitude='lat', longitude='lon', color='color', zoom=9)
        st.caption("🟡 Recycling Centers | 🔵 Neighbors | 🟢 Your Posts")
    else:
        st.warning("No items found in this area.")

with t3:
    st.subheader("National Feed")
    for item in reversed([d for d in filtered_data if d['user'] != "OFFICIAL"]):
        with st.container(border=True):
            st.write(f"**{item['name']}** - {item.get('area', 'Kuwait')}")
            st.caption(f"👤 {item['user']} | 🌱 {item.get('cat', 'Item')}")

with t4:
    st.subheader("🏆 Kuwait's Top Eco-Warriors")
    if user_items:
        rank_df = pd.DataFrame(user_items)
        rank_df['eco_num'] = 10 # Defaulting each post to 10kg
        ranking = rank_df.groupby('user')['eco_num'].sum().sort_values(ascending=False).reset_index()
        st.table(ranking.head(10))
