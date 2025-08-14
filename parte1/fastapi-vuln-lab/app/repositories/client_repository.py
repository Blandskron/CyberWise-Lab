from typing import List, Optional, Dict, Any
from datetime import datetime
from ..db import get_conn

# Repositorio deliberadamente vulnerable (concatenación de strings -> SQLi)

def list_clients() -> List[Dict[str, Any]]:
    con = get_conn()
    cur = con.cursor()
    cur.execute("SELECT id, name, email, notes, created_at FROM clients ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    return rows

def get_client(client_id: int) -> Optional[Dict[str, Any]]:
    con = get_conn()
    cur = con.cursor()
    cur.execute(f"SELECT id, name, email, notes, created_at FROM clients WHERE id = {client_id}")  # SQLi
    row = cur.fetchone()
    con.close()
    return dict(row) if row else None

def create_client(name: str, email: str, notes: Optional[str]) -> Dict[str, Any]:
    con = get_conn()
    cur = con.cursor()
    now = datetime.utcnow().isoformat()
    # SQLi por concatenación: **NO** usar en producción
    cur.execute(f"INSERT INTO clients (name, email, notes, created_at) VALUES ('{name}', '{email}', '{notes or ''}', '{now}')")
    con.commit()
    new_id = cur.lastrowid
    con.close()
    return {"id": new_id, "name": name, "email": email, "notes": notes, "created_at": now}

def update_client(client_id: int, name: str, email: str, notes: Optional[str]) -> Optional[Dict[str, Any]]:
    con = get_conn()
    cur = con.cursor()
    cur.execute(f"UPDATE clients SET name = '{name}', email = '{email}', notes = '{notes or ''}' WHERE id = {client_id}")  # SQLi
    con.commit()
    con.close()
    return get_client(client_id)

def delete_client(client_id: int) -> bool:
    con = get_conn()
    cur = con.cursor()
    cur.execute(f"DELETE FROM clients WHERE id = {client_id}")  # SQLi
    con.commit()
    changes = con.total_changes
    con.close()
    return changes > 0

def search_clients(q: str) -> List[Dict[str, Any]]:
    con = get_conn()
    cur = con.cursor()
    # SQLi de libro con LIKE
    sql = f"SELECT id, name, email, notes, created_at FROM clients WHERE name LIKE '%{q}%' OR email LIKE '%{q}%' OR notes LIKE '%{q}%' ORDER BY id DESC"
    cur.execute(sql)
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    return rows
