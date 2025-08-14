import os, sqlite3
from .config import settings

os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)

def get_conn():
    # Conexión simple, sin pool. Ideal para demo local.
    con = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_conn()
    cur = con.cursor()
    # Tabla con campos susceptibles a XSS (name/notes)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    ''')
    con.commit()
    con.close()
