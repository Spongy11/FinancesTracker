import psycopg2
import os
from datetime import datetime

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def init_database():
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
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
