import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import psycopg2
import os

st.set_page_config(page_title="Personal Finance Tracker", layout="wide", initial_sidebar_state="expanded")

def get_db_connection():
    """Connessione database che funziona sia in locale che su Streamlit Cloud"""
    try:
        # Prova prima con Streamlit secrets (deployment)
        if 'DATABASE_URL' in st.secrets:
            return psycopg2.connect(st.secrets['DATABASE_URL'])
        elif all(key in st.secrets for key in ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']):
            return psycopg2.connect(
                host=st.secrets['DB_HOST'],
                port=st.secrets.get('DB_PORT', '5432'),
                database=st.secrets['DB_NAME'],
                user=st.secrets['DB_USER'],
                password=st.secrets['DB_PASSWORD']
            )
    except:
        pass
    
    # Fallback per sviluppo locale
    if 'DATABASE_URL' in os.environ:
        return psycopg2.connect(os.environ['DATABASE_URL'])
    
    # Messaggio di errore se nessuna configurazione trovata
    st.error("⚠️ Database non configurato! Aggiungi DATABASE_URL nei Secrets di Streamlit Cloud.")
    st.stop()

# Inizializza le tabelle al primo avvio
@st.cache_resource
def init_database():
    """Crea le tabelle se non esistono"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id SERIAL PRIMARY KEY,
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id SERIAL PRIMARY KEY,
                amount DECIMAL(10, 2) NOT NULL,
                type VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                target_amount DECIMAL(10, 2) NOT NULL,
                current_amount DECIMAL(10, 2) DEFAULT 0,
                target_date DATE,
                category VARCHAR(100),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id SERIAL PRIMARY KEY,
                category VARCHAR(100) NOT NULL,
                monthly_limit DECIMAL(10, 2) NOT NULL,
                alert_threshold DECIMAL(5, 2) DEFAULT 80,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Errore inizializzazione database: {e}")
        return False

# Inizializza database
init_database()

# Resto del codice rimane identico...
def load_income_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, amount, category, date, description FROM income ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': row[0], 'amount': float(row[1]), 'category': row[2], 'date': row[3], 'description': row[4]} for row in rows]

# ... [resto del codice identico a prima] ...