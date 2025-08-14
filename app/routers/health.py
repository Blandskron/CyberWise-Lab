from fastapi import APIRouter
from ..observability.health import router as health_router
router = health_router
