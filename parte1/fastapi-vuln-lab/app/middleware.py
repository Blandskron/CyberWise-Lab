import random
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from .config import settings

class ChaosMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Inyecta fallos 500 con cierta probabilidad
        if settings.CHAOS_RATE > 0 and random.random() < settings.CHAOS_RATE:
            # Mensaje intencionalmente genérico (pero con detalles en logs)
            return PlainTextResponse("Internal Server Error (chaos)", status_code=500)
        response = await call_next(request)
        return response
