import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses
    (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, category TEXT, description TEXT, date TEXT)
    ''')
    conn.commit()
    conn.close()

def add_expense_to_db(user_id, amount, category, description):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
                   (user_id, amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses(user_id, period):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    if period == "diário":
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "semanal":
        start_date = datetime.now() - timedelta(days=7)
    elif period == "mensal":
        start_date = datetime.now() - timedelta(days=30)
    else:
        return None

    cursor.execute('''
    SELECT category, SUM(amount) 
    FROM expenses 
    WHERE user_id = ? AND date >= ? 
    GROUP BY category
    ''', (user_id, start_date.strftime("%Y-%m-%d %H:%M:%S")))
    
    results = cursor.fetchall()
    conn.close()
    return results