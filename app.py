import streamlit as st
import sqlite3
import pandas as pd
import time
import uuid
import re  # For regex (phone validation)

# --- 1. Database Functions ---
def init_db():
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, phone TEXT)''')
    
    # Items table
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id TEXT PRIMARY KEY, 
                  user TEXT, 
                  title TEXT, 
                  description TEXT, 
                  price REAL, 
                  contact TEXT,
                  image_path TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Comments/Offers table
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (id TEXT PRIMARY KEY,
                  item_id TEXT,
                  user TEXT,
                  comment TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('marketplace.db', check_same_thread=False)

# --- 2. Helper Functions ---

def sanitize_phone(phone_number, country_code):
    """
    Cleans phone number: removes spaces/dashes, ensures it starts with country code.
    Example: Input (123 45678, +965) -> Output 96512345678
    """
    if not phone_number:
        return None
    
    # Remove all non-numeric characters
    clean_num = re.sub(r'\D', '', phone_number)
    
    # Remove the country code if the user typed it manually to avoid duplication
    # (e.g., if user typed 96512345, we don't want to add 965 again to make 965965...)
    clean_code = re.sub(r'\D', '', country_code)
    
    if clean_num.startswith(clean_code):
        return clean_num
    else:
        return clean_code + clean_num

def signup_user(username, password, phone, country_code):
    conn = get_db_connection()
    c = conn.cursor()
    
    final_phone = sanitize_phone(phone, country_code)
    
    try:
        c.execute("INSERT INTO users (username, password, phone) VALUES (?, ?, ?)", 
                  (username, password, final_phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT password, phone FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == password:
        return result[1] # Return the phone number
    return None

def create_item(user, title, description, price, contact, image):
    conn = get_db_connection()
    c = conn.cursor()
    item_id = str(uuid.uuid4())
    
    # In a real app, you would save the 'image' file to disk or cloud storage (S3).
    # For this MVP, we will assume 'image' is just the filename or we skip saving binary data to DB for simplicity.
    # We will just store the filename if provided.
    image_name = image.name if image else "placeholder.png"
    
    c.execute("INSERT INTO items (id, user, title, description, price, contact, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (item_id, user, title, description, price, contact, image_name))
    conn.commit()
    conn.close()

def get_items():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM items ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def add_comment(item_id, user, comment_text):
    conn = get_db_connection()
    c = conn.cursor()
    comment_id = str(uuid.uuid4())
    c.execute("INSERT INTO comments (id, item_id, user, comment) VALUES (?, ?, ?, ?)",
              (comment_id, item_id, user, comment_text))
    conn.commit()
    conn.close()

def get_comments(item_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user, comment, timestamp FROM comments WHERE item_id=? ORDER BY timestamp ASC", (item_id,))
    data = c.fetchall()
    conn.close()
    return data

# --- 3. Main App Logic ---

def main():
    st.set_page_config(page_title="Community Market", page_icon="🛒", layout="wide")
    
    # Hide Streamlit Branding
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    init_db()

    # Session State for Login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['user_phone'] = None

    # --- SIDEBAR (Login/Signup & Founder Msg) ---
    with st.sidebar:
        st.title("📱 EcoScan Market")
        
        if not st.session_state['logged_in']:
            tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
            
            with tab_login:
                login_user = st.text_input("Username", key="login_user")
                login_pass = st.text_input("Password", type="password", key="login_pass")
                if st.button("Log In"):
                    phone_found = check_login(login_user, login_pass)
                    if phone_found:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = login_user
                        st.session_state['user_phone'] = phone_found
                        st.success(f"Welcome back, {login_user}!")
                        st.rerun()
                    else:
                        st.error("Incorrect username or password")
            
            with tab_signup:
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                
                # Enhanced Phone Input
                col_code, col_num = st.columns([1, 2])
                with col_code:
                    country_code = st.selectbox("Code", ["+965", "+966", "+971", "+974", "+20", "+1", "+44"], index=0)
                with col_num:
                    new_phone = st.text_input("Mobile Number")

                if st.button("Sign Up"):
                    if new_user and new_pass and new_phone:
                        if signup_user(new_user, new_pass, new_phone, country_code):
                            st.success("Account created! Please log in.")
                        else:
                            st.error("Username already exists.")
                    else:
                        st.warning("Please fill all fields.")
        
        else:
            st.success(f"Logged in as: {st.session_state['username']}")
            if st.button("Log Out"):
                st.session_state['logged_in'] = False
                st.session_state['username'] = None
                st.session_state['user_phone'] = None
                st.rerun()

        # --- FOUNDER MESSAGE SECTION ---
        st.divider()
        st.subheader("👋 From the Founder")
        
        # Display image from root directory
        try:
            st.image("founder.jpeg", caption="Founder's Note", use_container_width=True)
        except:
            st.info("(founder.jpeg not found)")
            
        st.info("Welcome to our community! We built this platform to make buying and selling simple, transparent, and direct. Thank you for being a part of our journey.")
        # -------------------------------

    # --- MAIN CONTENT AREA ---
    
    # Define Tabs
    if st.session_state['logged_in']:
        tab1, tab2, tab3 = st.tabs(["🛍️ Buy Items", "➕ Sell Item", "👤 Profile"])
    else:
        tab1 = st.container() # Only show Buy tab if not logged in (simulated via container)
        st.subheader("🛍️ Buy Items")
        # If not logged in, we only show items. Sell/Profile are hidden or prompting login.

    # -- TAB 1: BUY ITEMS (Feed) --
    with tab1:
        st.markdown("### Latest Listings")
        
        # Search Bar
        search_query = st.text_input("🔍 Search items...", "")
        
        items = get_items()
        
        if search_query:
            items = items[items['title'].str.contains(search_query, case=False, na=False)]

        if items.empty:
            st.info("No items found.")
        else:
            for index, row in items.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([1, 3])
                    
                    with c1:
                        # Placeholder logic for images
                        st.image("https://via.placeholder.com/150?text=Item", use_container_width=True)
                    
                    with c2:
                        st.subheader(row['title'])
                        st.write(f"**Price:** {row['price']} KD")
                        st.write(row['description'])
                        st.caption(f"Seller: {row['user']} | Posted: {row['timestamp']}")
                        
                        # --- HYBRID CONTACT BUTTONS ---
                        col_wa, col_cmt = st.columns([1, 1])
                        
                        with col_wa:
                            # WhatsApp Direct Link
                            wa_message = f"Hi, I am interested in your item: {row['title']}"
                            # row['contact'] is the phone number from DB
                            wa_link = f"https://wa.me/{row['contact']}?text={wa_message.replace(' ', '%20')}"
                            
                            st.link_button("💬 Chat on WhatsApp", wa_link, type="primary")

                        # --- INTERNAL COMMENTS SECTION ---
                        with st.expander(f"💬 Offers & Comments ({row['id'][:4]}...)"):
                            # Show existing comments
                            existing_comments = get_comments(row['id'])
                            for c_user, c_text, c_time in existing_comments:
                                st.text(f"{c_user}: {c_text}")
                            
                            if st.session_state['logged_in']:
                                # Add new comment
                                new_comment = st.text_input(f"Write an offer for {row['title']}", key=f"c_{row['id']}")
                                if st.button("Post", key=f"btn_{row['id']}"):
                                    if new_comment:
                                        add_comment(row['id'], st.session_state['username'], new_comment)
                                        st.success("Sent!")
                                        time.sleep(1)
                                        st.rerun()
                            else:
                                st.caption("Log in to post offers.")

    # -- TAB 2: SELL ITEM (Only if logged in) --
    if st.session_state['logged_in']:
        with tab2:
            st.header("List a New Item")
            
            with st.form("sell_form", clear_on_submit=True):
                title = st.text_input("Item Title")
                desc = st.text_area("Description")
                price = st.number_input("Price (KD)", min_value=0.0, step=0.5)
                photo = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])
                
                submitted = st.form_submit_button("Publish Listing")
                
                if submitted:
                    if title and price > 0:
                        # Use the logged-in user's phone number automatically
                        user_phone = st.session_state['user_phone']
                        
                        create_item(st.session_state['username'], title, desc, price, user_phone, photo)
                        st.balloons()
                        st.success("Item listed successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Please provide a title and price.")

    # -- TAB 3: PROFILE (Only if logged in) --
    if st.session_state['logged_in']:
        with tab3:
            st.header("My Profile")
            st.write(f"**Username:** {st.session_state['username']}")
            st.write(f"**Registered Phone:** {st.session_state['user_phone']}")
            st.info("Your phone number is hidden from public view, but the WhatsApp button on your items will link to it.")

if __name__ == "__main__":
    main()
