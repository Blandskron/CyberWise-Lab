import time, logging, uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from .processors import enrich
from .sinks import filebeat_fmt


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start = time.perf_counter()
        try:
            response = await call_next(request)
            status = response.status_code
            error = None
        except Exception as exc:
            status = 500
            error = {"type": type(exc).__name__, "msg": str(exc)}
            raise
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            event = enrich({
                "rid": rid,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.url.query),
                "ip": request.client.host if request.client else None,
                "ua": request.headers.get("user-agent"),
                "status": status,
                "latency_ms": round(elapsed,2),
                "error": error,
            })
            filebeat_fmt.emit(event)
        return response
