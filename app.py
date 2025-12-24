import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- 1. SENDER CONFIGURATION ---
# Use your professional email and an App Password from Google
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"

def send_welcome_email(user_email, user_name):
    try:
        # Create the email container
        msg = MIMEMultipart()
        msg['From'] = f"EcoScan Kuwait <{SENDER_EMAIL}>"
        msg['To'] = user_email
        msg['Subject'] = f"Welcome to the Movement, {user_name}! 🌱"

        # The Email Content
        body = f"""
        <html>
        <body>
            <h2>Marhaba, {user_name}! 🇰🇼</h2>
            <p>Thank you for joining <b>EcoScan Kuwait</b>. You are now part of a community dedicated to a greener future.</p>
            <h3>How to get started:</h3>
            <ul>
                <li><b>Post an Item:</b> Earn 10 Eco-Points for every item you list.</li>
                <li><b>Request a Swap:</b> Find items in Hawalli, Asimah, and beyond.</li>
                <li><b>Climb the Leaderboard:</b> Compete with others to be the top Eco-Warrior.</li>
            </ul>
            <p>Happy Swapping!<br><b>Abilash Vani</b><br>Founder, EcoScan Kuwait</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

# --- 2. UPDATED REGISTRATION INTERFACE ---
if st.session_state.view == "signup":
    st.subheader("Create Your Eco-Warrior Account")
    with st.form("signup_form"):
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email Address (for welcome guide)")
        new_phone = st.text_input("Mobile Number")
        new_area = st.selectbox("Governorate", ["Asimah", "Hawalli", "Farwaniya", "Ahmadi", "Jahra", "Mubarak"])
        new_pw = st.text_input("Password", type="password")
        
        if st.form_submit_button("Join & Get 10 Points"):
            if new_name and new_email and new_phone:
                # 1. Save to Database
                users = load_data(USER_DB)
                users.append({
                    "name": new_name, "email": new_email, "phone": new_phone, 
                    "area": new_area, "password": new_pw, "points": 10
                })
                save_data(USER_DB, users)
                
                # 2. Send the Welcome Email
                with st.spinner("Sending your welcome guide..."):
                    send_welcome_email(new_email, new_name)
                
                st.success("Account created! Check your inbox for your welcome guide.")
                st.session_state.view = "login"
                st.rerun()
            else:
                st.warning("Please fill in all fields.")
