from prometheus_client import Counter, Histogram

# KPI Counters
REQUESTS = Counter("api_requests_total", "Total de requests", ["method","path","status"])
WRITES  = Counter("api_write_ops_total", "Operaciones de escritura", ["method","path","status","ip"])
ERROR5 = Counter("api_errors_5xx_total", "Errores 5xx")
ERROR4 = Counter("api_errors_4xx_total", "Errores 4xx")

# Latencia por ruta
LATENCY = Histogram("api_request_seconds", "Latencia por request en segundos", ["method","path"])
