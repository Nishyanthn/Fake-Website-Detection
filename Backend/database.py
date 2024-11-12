import sqlite3

# Function to connect to the database
def connect_db():
    return sqlite3.connect('suspicious_urls.db')

# Function to create the table (you can call this once when you first run the app)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suspicious_urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        is_live BOOLEAN
    )
    ''')
    conn.commit()
    conn.close()

# Function to insert a URL into the database
def insert_url(url, is_live):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO suspicious_urls (url, is_live) VALUES (?, ?)
    ''', (url, is_live))
    conn.commit()
    conn.close()

# Function to fetch all URLs from the database
def fetch_urls():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suspicious_urls')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to update the live status of a URL
def update_url_status(url, is_live):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE suspicious_urls SET is_live = ? WHERE url = ?
    ''', (is_live, url))
    conn.commit()
    conn.close()
