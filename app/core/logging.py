import logging, json, os, sys
from logging.handlers import RotatingFileHandler
from .config import settings

class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        for f in ("asctime","pathname","lineno","funcName"):
            base[f] = getattr(record, f, None)
        if hasattr(record, "extra"):
            base.update(record.extra)
        return json.dumps(base, ensure_ascii=False)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logger.level)
    ch.setFormatter(JsonFormatter() if settings.LOG_JSON else logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(ch)

    # File handler (rotate)
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
    fh = RotatingFileHandler(settings.LOG_FILE, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logger.level)
    fh.setFormatter(JsonFormatter() if settings.LOG_JSON else logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(fh)
