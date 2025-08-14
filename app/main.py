from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from .core.logging import setup_logging
from .middleware.request_id import RequestIdMiddleware
from .observability.metrics import MetricsMiddleware
from .middleware.cors import build_cors
from .audit.middleware import AuditMiddleware
from .routers import metrics as metrics_router, health as health_router
from .routers import clients
from .db import init_db

setup_logging()
init_db()

app = FastAPI(title="fastapi-vuln-lab (obs/audit)", version="0.1.0")

cors_cfg = build_cors()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_cfg["allow_origins"],
    allow_credentials=cors_cfg["allow_credentials"],
    allow_methods=cors_cfg["allow_methods"],
    allow_headers=cors_cfg["allow_headers"],
)

if settings.ENABLE_REQUEST_ID:
    app.add_middleware(RequestIdMiddleware)
if settings.ENABLE_AUDIT:
    app.add_middleware(AuditMiddleware)
if settings.ENABLE_METRICS:
    app.add_middleware(MetricsMiddleware)

app.include_router(clients.router)
if settings.ENABLE_HEALTH:
    app.include_router(health_router.router)
if settings.ENABLE_METRICS:
    app.include_router(metrics_router.router)
