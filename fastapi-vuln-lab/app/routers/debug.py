from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/random-500")
def random_500():
    # Fallo explícito para tests
    raise RuntimeError("Error intencional para pruebas de manejo de 500")

@router.get("/echo")
def echo(text: Optional[str] = Query(None, alias="text")):
    # Endpoint que refleja el valor (posible XSS si el cliente lo inserta en DOM sin sanitizar)
    if text is None:
        return {"echo": None}
    # Simulamos error con 500 si se pasa cierto texto
    if text.lower() == "explode":
        raise HTTPException(status_code=500, detail=f"Explosión: {text}")
    return {"echo": text}
