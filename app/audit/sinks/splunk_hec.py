import logging, os, requests

log = logging.getLogger("splunk")
HEC_URL = os.getenv("SPLUNK_HEC_URL", "")
HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN", "")

def emit(event: dict):
    if not HEC_URL or not HEC_TOKEN:
        log.debug("splunk_hec_disabled", extra={"extra": event})
        return
    headers = {"Authorization": f"Splunk {HEC_TOKEN}"}
    data = {"event": event}
    try:
        requests.post(HEC_URL, json=data, headers=headers, timeout=2)
    except Exception as e:
        log.warning("splunk_hec_error", extra={"extra": {"error": str(e)}})
