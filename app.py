import streamlit as st
import sqlite3
import pandas as pd
import time
import uuid
import re

# --- 1. Database Functions ---
def init_db():
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, phone TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, user TEXT, title TEXT, description TEXT, price REAL, contact TEXT, image_path TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments (id TEXT PRIMARY KEY, item_id TEXT, user TEXT, comment TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('marketplace.db', check_same_thread=False)

def sanitize_phone(phone_number, country_code):
    if not phone_number: return None
    clean_num = re.sub(r'\D', '', phone_number)
    clean_code = re.sub(r'\D', '', country_code)
    if clean_num.startswith(clean_code): return clean_num
    else: return clean_code + clean_num

def signup_user(username, password, phone, country_code):
    conn = get_db_connection()
    c = conn.cursor()
    final_phone = sanitize_phone(phone, country_code)
    try:
        c.execute("INSERT INTO users (username, password, phone) VALUES (?, ?, ?)", (username, password, final_phone))
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
    if result and result[0] == password: return result[1]
    return None

def create_item(user, title, description, price, contact, image):
    conn = get_db_connection()
    c = conn.cursor()
    item_id = str(uuid.uuid4())
    image_name = image.name if image else "placeholder.png"
    
    # Safe execute
    sql = "INSERT INTO items (id, user, title, description, price, contact, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)"
    val = (item_id, user, title, description, price, contact, image_name)
    c.execute(sql, val)
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
    
    # Safe execute
    sql = "INSERT INTO comments (id, item_id, user, comment) VALUES (?, ?, ?, ?)"
    val = (comment_id, item_id, user, comment_text)
    c.execute(sql, val)
    conn.commit()
    conn.close()

def get_comments(item_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Safe execute
    sql = "SELECT user, comment, timestamp FROM comments WHERE item_id=? ORDER BY timestamp ASC"
    c.execute(sql, (item_id,))
    
    data = c.fetchall()
    conn.close()
    return data

# --- 2. Main App Logic ---

def main():
    st.set_page_config(page_title="EcoScan Market", page_icon="📱", layout="wide")
    
    # Hide standard Streamlit header/footer
    hide_st_style = """*
