import streamlit as st
from PIL import Image
import pandas as pd
import json
import os

# 1. PAGE CONFIG (The "Favicon" & Layout)
st.set_page_config(
    page_title="EcoScan Pro: Salmiya", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Database & Config ---
DB_FILE = "items_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return [
        {"name": "Bicycle", "user": "Ahmad", "lat": 29.3375, "lon": 48.0750, "eco": "22kg", "cat": "Sports"},
        {"name": "Bookshelf", "user": "Fatima", "lat": 29.3420, "lon": 48.0820, "eco": "15kg", "cat": "Furniture"}
    ]

def save_item(name, user, lat, lon, eco, cat):
    data = load_data()
    data.append({"name": name, "user": user, "lat": lat, "lon": lon, "eco": eco, "cat": cat})
    with open(DB_FILE, "w") as f: json.dump(data, f)

# --- Sidebar Impact & Sharing ---
data = load_data()
st.sidebar.title("🌍 Salmiya Impact")
st.sidebar.metric(label="CO2 Prevented", value=f"{5120 + (len(data)*5)} kg", delta="12%")

share_text = f"I just saved {5120 + (len(data)*5)}kg of CO2 using EcoScan Salmiya! 🌱"
st.sidebar.markdown(f"[![Share on WhatsApp](https://img.shields.io/badge/Share-WhatsApp-25D366?style=for-the-badge&logo=whatsapp)](https://api.whatsapp.com/send?text={share_text})")

# NEW: Category Filter in Sidebar
st.sidebar.subheader("🔍 Filter by Category")
categories = ["All", "Furniture", "Electronics", "Clothes", "Sports", "Other"]
selected_cat = st.sidebar.selectbox("Show me:", categories)

# Filter the data based on selection
if selected_cat == "All":
    filtered_data = data
else:
    filtered_data = [d for d in data if d.get('cat') == selected_cat]

# --- Main App ---
st.title("🌱 EcoScan & Swap")
t1, t2, t3 = st.tabs(["📤 Scan & Post", "📍 Salmiya Map", "📱 Feed"])

with t1:
    st.subheader("Post an Item")
    item_cat = st.selectbox("Select Category", categories[1:]) # Don't show "All" here
    up = st.file_uploader("Scan item photo", type=["jpg", "png", "jpeg"])
    if up:
        st.image(Image.open(up), width=300)
        if st.button("Confirm & Post to Salmiya"):
            # Saves with the selected category
            save_item(up.name.split('.')[0], "You", 29.33 + (len(data)*0.001), 48.07 + (len(data)*0.001), "10kg", item_cat)
            st.success(f"{up.name.split('.')[0]} posted in {item_cat}!")
            st.balloons()

with t2:
    st.subheader(f"Neighborhood Map: {selected_cat}")
    if not filtered_data:
        st.warning("No items found in this category yet!")
    else:
        map_df = pd.DataFrame(filtered_data)
        map_df['color'] = map_df['user'].apply(lambda x: '#0000FF' if x != 'You' else '#00FF00')
        st.map(map_df, latitude='lat', longitude='lon', color='color', zoom=13)
        st.caption("🟢 Green: Your Posts | 🔵 Blue: Neighbors")

with t3:
    st.subheader(f"Recent Swaps ({selected_cat})")
    for item in reversed(filtered_data):
        with st.container(border=True):
            st.write(f"**{item['name']}** ({item['cat']})")
            st.caption(f"👤 {item['user']} | 🌱 {item['eco']} Saved")
            st.button("Message Neighbor", key=f"btn_{item['name']}_{item['user']}")
