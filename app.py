import streamlit as st
from PIL import Image
import pandas as pd
import json
import os
from fpdf import FPDF

# 1. PAGE CONFIG
st.set_page_config(page_title="EcoScan Pro: Salmiya", page_icon="🌱", layout="wide")

# --- Database & Config ---
DB_FILE = "items_db.json"
RECYCLING_CENTERS = [
    {"name": "Salmiya Block 4 Drop-off", "user": "OFFICIAL CENTER", "lat": 29.3325, "lon": 48.0680, "eco": 0, "cat": "Recycling"},
    {"name": "Salmiya Co-op Collection", "user": "OFFICIAL CENTER", "lat": 29.3415, "lon": 48.0730, "eco": 0, "cat": "Recycling"}
]

def load_data():
    user_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: user_data = json.load(f)
    if not user_data:
        user_data = [
            {"name": "Bicycle", "user": "Fatima", "lat": 29.3375, "lon": 48.0750, "eco": "50kg", "cat": "Sports"},
            {"name": "Bookshelf", "user": "Ali", "lat": 29.3420, "lon": 48.0820, "eco": "30kg", "cat": "Furniture"}
        ]
    return user_data + RECYCLING_CENTERS

def save_item(name, user, lat, lon, eco, cat):
    current_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: current_data = json.load(f)
    current_data.append({"name": name, "user": user, "lat": lat, "lon": lon, "eco": eco, "cat": cat})
    with open(DB_FILE, "w") as f: json.dump(current_data, f)

# --- Logic: Search & Filter ---
full_data = load_data()
user_items = [d for d in full_data if d['user'] != "OFFICIAL CENTER"]

# Sidebar Search & Filter
st.sidebar.title("🌍 Salmiya Impact")
search_query = st.sidebar.text_input("🔍 Search items (e.g. 'bike')", "").lower()
selected_cat = st.sidebar.selectbox("Category:", ["All", "Furniture", "Electronics", "Clothes", "Sports", "Recycling"])

# Apply Search and Category Filters
filtered_data = [
    d for d in full_data 
    if (search_query in d['name'].lower()) and 
    (selected_cat == "All" or d['cat'] == selected_cat)
]

# --- Sidebar Metrics ---
leaderboard_df = pd.DataFrame(user_items)
leaderboard_df['eco_num'] = leaderboard_df['eco'].apply(lambda x: int(str(x).replace('kg','')))
ranking = leaderboard_df.groupby('user')['eco_num'].sum().sort_values(ascending=False).reset_index()
total_saved = 5120 + ranking['eco_num'].sum()
st.sidebar.metric(label="Neighborhood Total", value=f"{total_saved} kg")

# --- Main App ---
st.title("🌱 EcoScan & Swap")
t1, t2, t3, t4, t5 = st.tabs(["📤 Scan", "📍 Map", "📱 Feed", "🏆 Leaderboard", "📜 Certificate"])

with t1:
    st.subheader("Post an Item")
    item_cat = st.selectbox("Category", ["Furniture", "Electronics", "Clothes", "Sports"])
    up = st.file_uploader("Scan item photo", type=["jpg", "png", "jpeg"])
    if up:
        if st.button("Confirm & Post"):
            save_item(up.name.split('.')[0], "You", 29.33 + (len(user_items)*0.005), 48.07 + (len(user_items)*0.005), "10kg", item_cat)
            st.success("Item posted!")
            st.balloons()

with t2:
    st.subheader(f"Map Results: '{search_query}'")
    if filtered_data:
        map_df = pd.DataFrame(filtered_data)
        map_df['color'] = map_df['user'].apply(lambda x: '#FFFF00' if x == "OFFICIAL CENTER" else ('#00FF00' if x == "You" else '#0000FF'))
        st.map(map_df, latitude='lat', longitude='lon', color='color', zoom=13)
    else:
        st.warning("No matches found on the map.")

with t3:
    st.subheader("Neighborhood Feed")
    display_feed = [d for d in filtered_data if d['user'] != "OFFICIAL CENTER"]
    if not display_feed:
        st.info("No items match your search.")
    for item in reversed(display_feed):
        with st.container(border=True):
            st.write
