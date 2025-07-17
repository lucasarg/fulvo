import sqlite3

def init_db():
    conn = sqlite3.connect('basedatos.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        posicion TEXT NOT NULL,
        numero INTEGER NOT NULL,
        equipo TEXT
    )
    """)
    
    conn.commit()
    conn.close()
