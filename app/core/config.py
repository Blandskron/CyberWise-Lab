import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "fastapi-vuln-lab")
    ENV: str = os.getenv("ENV", "lab")  # lab | safe
    PORT: int = int(os.getenv("PORT", "8000"))

    # Feature toggles
    ENABLE_HEALTH: bool = os.getenv("ENABLE_HEALTH", "true").lower() == "true"
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    ENABLE_AUDIT: bool = os.getenv("ENABLE_AUDIT", "true").lower() == "true"
    ENABLE_REQUEST_ID: bool = os.getenv("ENABLE_REQUEST_ID", "true").lower() == "true"

    # Security toggles (for Part 4 mitigation)
    SQL_PARAMS_ON: bool = os.getenv("SQL_PARAMS_ON", "false").lower() == "true"
    XSS_ESCAPE_ON: bool = os.getenv("XSS_ESCAPE_ON", "false").lower() == "true"
    CORS_SAFE_ON: bool = os.getenv("CORS_SAFE_ON", "false").lower() == "true"

    # Observabilidad
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_JSON: bool = os.getenv("LOG_JSON", "true").lower() == "true"
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

    # Exporters / sinks
    LOGSTASH_URL: str = os.getenv("LOGSTASH_URL", "http://localhost:5044")
    SPLUNK_HEC_URL: str = os.getenv("SPLUNK_HEC_URL", "http://localhost:8088/services/collector")
    SPLUNK_HEC_TOKEN: str = os.getenv("SPLUNK_HEC_TOKEN", "disabled")

settings = Settings()
