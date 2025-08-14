import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from ..core.kpi import REQUESTS, WRITES, LATENCY, ERROR5, ERROR4

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed = time.perf_counter() - start

        path = request.url.path
        method = request.method
        status = response.status_code

        REQUESTS.labels(method=method, path=path, status=str(status)).inc()
        LATENCY.labels(method=method, path=path).observe(elapsed)
        if 500 <= status <= 599:
            ERROR5.inc()
        if 400 <= status <= 499:
            ERROR4.inc()

        if method in ("POST","PUT","PATCH","DELETE"):
            ip = request.client.host if request.client else "unknown"
            WRITES.labels(method=method, path=path, status=str(status), ip=ip).inc()

        return response
