from .config import settings

def sql_params_enabled() -> bool:
    return settings.SQL_PARAMS_ON

def xss_escape_enabled() -> bool:
    return settings.XSS_ESCAPE_ON

def cors_safe_enabled() -> bool:
    return settings.CORS_SAFE_ON
