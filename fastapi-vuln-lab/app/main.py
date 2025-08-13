from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .config import settings
from .middleware import ChaosMiddleware
from .db import init_db
from .routers import clients, auth, debug

init_db()

app = FastAPI(
    title="FastAPI Vulnerable Lab",
    version="0.1.0",
    description="API intencionalmente vulnerable para prácticas de ciberseguridad (XSS, CSRF, SQLi, errores 500). No usar en producción."
)

# CORS excesivamente permisivo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # cualquier origen
    allow_credentials=True,        # junto con * -> riesgoso (eco del origin)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cookie de sesión sin CSRF ni seguridad robusta
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Inyección de fallos 500 "raros"
app.add_middleware(ChaosMiddleware)

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}

# Routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(debug.router)
