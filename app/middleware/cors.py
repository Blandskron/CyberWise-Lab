from fastapi.middleware.cors import CORSMiddleware
from ..core.security_flags import cors_safe_enabled

def build_cors():
    if cors_safe_enabled():
        return {
            "allow_origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "allow_credentials": False,
            "allow_methods": ["GET","POST","PUT","DELETE"],
            "allow_headers": ["*"],
        }
    else:
        return {
            "allow_origins": ["*"],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
