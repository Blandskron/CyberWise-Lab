from typing import Dict
from datetime import datetime

def enrich(base: Dict) -> Dict:
    base["ts"] = datetime.utcnow().isoformat()
    base.setdefault("service", "fastapi-vuln-lab")
    return base
