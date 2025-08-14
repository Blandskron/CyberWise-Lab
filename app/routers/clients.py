from typing import Optional
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel

from ..services import client_service
from ..utils.html_templates import render_clients_table

router = APIRouter(prefix="/clients", tags=["clients"])

class ClientCreate(BaseModel):
    name: str
    email: str
    notes: Optional[str] = None

class ClientUpdate(BaseModel):
    name: str
    email: str
    notes: Optional[str] = None

@router.get("")
def list_clients():
    return client_service.list_clients()

@router.get("/{client_id}")
def get_client(client_id: int):
    c = client_service.get_client(client_id)
    if not c:
        raise HTTPException(404, "client no encontrado")
    return c

# CRUD ABIERTO (sin login)
@router.post("")
def create_client(payload: ClientCreate):
    return client_service.create_client(payload.name, payload.email, payload.notes)

# Variante tipo formulario (útil para orquestar ataques desde otro origen)
@router.post("/form")
def create_client_form(
    name: str = Form(...),
    email: str = Form(...),
    notes: Optional[str] = Form(None),
):
    return client_service.create_client(name, email, notes)

@router.put("/{client_id}")
def update_client(client_id: int, payload: ClientUpdate):
    c = client_service.update_client(client_id, payload.name, payload.email, payload.notes)
    if not c:
        raise HTTPException(404, "client no encontrado")
    return c

@router.put("/{client_id}/form")
def update_client_form(
    client_id: int,
    name: str = Form(...),
    email: str = Form(...),
    notes: Optional[str] = Form(None),
):
    c = client_service.update_client(client_id, name, email, notes)
    if not c:
        raise HTTPException(404, "client no encontrado")
    return c

@router.delete("/{client_id}")
def delete_client(client_id: int):
    ok = client_service.delete_client(client_id)
    if not ok:
        raise HTTPException(404, "client no encontrado")
    return {"deleted": ok}

# Vulnerabilidades extra
@router.get("/search")
def search(q: str):
    # **SQLi** por concatenación en el repositorio
    return {"q": q, "results": client_service.search_clients(q)}

@router.get("/render")
def render():
    # **XSS almacenado**: renderiza HTML sin escapar
    rows = client_service.list_clients()
    html = render_clients_table(rows)
    from fastapi import Response
    return Response(content=html, media_type="text/html")
