import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
import time
import random
import io

# --- Page Config ---
st.set_page_config(page_title="EcoScan Leader", page_icon="🌱", layout="wide")

# --- Memory & State ---
if "messages" not in st.session_state: st.session_state.messages = []
if "show_chat" not in st.session_state: st.session_state.show_chat = False
if "swap_complete" not in st.session_state: st.session_state.swap_complete = False

# --- Sidebar: Global Impact ---
st.sidebar.title("🌍 Global Impact")
st.sidebar.metric(label="Items Swapped Today", value="1,284", delta="12% vs Yesterday")
st.sidebar.metric(label="CO2 Prevented", value="5,120 kg")
st.sidebar.divider()
st.sidebar.subheader("🏆 Eco-Warrior Leaderboard")
st.sidebar.table({"Neighbor": ["Fatima", "Ali", "Zaid", "You"], "Points": [1420, 1100, 850, 120]})

# --- Function: Create Impact Certificate ---
def create_certificate(name, co2_saved):
    # Create a simple high-res certificate image
    img = Image.new('RGB', (800, 500), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # Green eco-border
    d.rectangle([20, 20, 780, 480], outline=(76, 175, 80), width=15)
    # Add Text (Simple version for compatibility)
    d.text((280, 100), "OFFICIAL ECO-HERO", fill=(0, 0, 0))
    d.text((280, 200), f"Awarded to: {name}", fill=(0, 0, 0))
    d.text((280, 250), f"Total Impact: {co2_saved}kg CO2 Saved", fill=(76, 175, 80))
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- Main App ---
st.title("🌱 EcoScan & Swap: Market Leader Edition")

tab1, tab2 = st.tabs(["📤 Scan & Swap", "📱 Neighborhood Feed"])

with tab1:
    uploaded_file = st.file_uploader("Scan an item to begin:", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        c1, c2 = st.columns([1, 1])
        with c1: st.image(Image.open(uploaded_file), use_container_width=True)
        with c2:
            st.success("✅ **AI Detected:** High-quality swap item!")
            if st.button("Message Matches in Salmiya"):
                st.session_state.show_chat = True
                st.toast("Sarah notified!")

    st.divider()
    st.subheader("📍 Real-time Neighbor Heatmap")
    my_lat, my_lon = 29.332, 48.068
    map_data = pd.DataFrame({'lat': [my_lat, my_lat+0.005, my_lat-0.003], 'lon': [my_lon, my_lon+0.004, my_lon-0.002]})
    st.map(map_data)

with tab2:
    st.subheader("👀 Trending in Salmiya")
    items = [
        {"name": "Office Chair", "user": "Sarah", "dist": "0.4mi", "eco": "15kg"},
        {"name": "Kids Bicycle", "user": "Ahmad", "dist": "0.8mi", "eco": "22kg"}
    ]
    for item in items:
        with st.container(border=True):
            st.write(f"**{item['name']}** - posted by {item['user']}")
            st.caption(f"📍 {item['dist']} away | 🌱 Saves {item['eco']} CO2")

# --- Chat & Certificate Logic ---
if st.session_state.show_chat:
    st.divider()
    with st.expander("💬 Conversation with Sarah", expanded=True):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.write(msg["content"])
        
        if p := st.chat_input("Say something to confirm the swap..."):
            st.session_state.messages.append({"role": "user", "content": p})
            st.session_state.messages.append({"role": "assistant", "content": "Deal! I'll see you tomorrow at 5 PM! 🤝"})
            st.session_state.swap_complete = True
            st.rerun()

        if st.session_state.swap_complete:
            st.balloons()
            st.success("Swap Confirmed! You've officially saved more carbon today than 90% of people.")
            cert = create_certificate("Salmiya Hero", random.randint(5, 25))
            st.download_button(label="📥 Download My Impact Certificate", data=cert, file_name="eco_certificate.png", mime="image/png")