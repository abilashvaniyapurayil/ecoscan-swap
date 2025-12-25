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
