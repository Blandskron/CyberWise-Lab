import logging
log = logging.getLogger("elk")

def emit(event: dict):
    # Stub de envío a Logstash vía HTTP si tuvieras un endpoint.
    # Normalmente se usa Filebeat. Lo dejamos para futura extensión.
    log.debug("elk_stub_event", extra={"extra": event})
