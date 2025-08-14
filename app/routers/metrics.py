from fastapi import APIRouter
from ..observability.exporters.prometheus import router as metrics_router
router = metrics_router
