from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware import ChaosMiddleware
from .db import init_db
from .routers import clients

init_db()

app = FastAPI(
    title="FastAPI Vulnerable Lab",
    version="0.2.0",
    description=(
        "API intencionalmente vulnerable para prácticas de ciberseguridad "
        "(XSS, SQLi, errores 500). Sin autenticación ni endpoints de salud/metrics."
    ),
)

# CORS excesivamente permisivo (sin autenticación, súper riesgoso por diseño)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inyección de fallos 500 "raros"
app.add_middleware(ChaosMiddleware)

# Solo el CRUD (con vulnerabilidades)
app.include_router(clients.router)
