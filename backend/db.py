import sqlite3

def create_db():
    conn=sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
                      CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            size REAL,
            bedrooms INTEGER,
            age INTEGER,
            location TEXT,
            predicted_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
                   """)
    
    conn.commit()
    conn.close()
    
create_db()