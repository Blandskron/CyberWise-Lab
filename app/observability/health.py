from fastapi import APIRouter
from app.db import get_conn

router = APIRouter(prefix="/health", tags=["meta"])

@router.get("")
def health():
    try:
        con = get_conn()
        cur = con.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        con.close()
        db_ok = True
    except Exception:
        db_ok = False

    return {"status":"ok" if db_ok else "degraded","db":db_ok}
