import logging, json

log = logging.getLogger("audit")

def emit(event: dict):
    # Formato JSON por línea; apto para Filebeat o lectura directa
    log.info(json.dumps(event, ensure_ascii=False), extra={"extra": event})
