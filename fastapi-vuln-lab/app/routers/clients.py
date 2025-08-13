from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from pydantic import BaseModel
from ..services import client_service
from ..utils.html_templates import render_clients_table

router = APIRouter(prefix="/clients", tags=["clients"])

def require_login(request: Request):
    user = request.cookies.get("session")
    if not user:
        raise HTTPException(status_code=401, detail="login requerido (cookie 'session')")
    return user

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

@router.post("", dependencies=[Depends(require_login)])
def create_client(payload: ClientCreate):
    return client_service.create_client(payload.name, payload.email, payload.notes)

# Variante vulnerable a CSRF vía formulario
@router.post("/form", dependencies=[Depends(require_login)])
def create_client_form(
    name: str = Form(...),
    email: str = Form(...),
    notes: Optional[str] = Form(None),
):
    return client_service.create_client(name, email, notes)

@router.put("/{client_id}", dependencies=[Depends(require_login)])
def update_client(client_id: int, payload: ClientUpdate):
    c = client_service.update_client(client_id, payload.name, payload.email, payload.notes)
    if not c:
        raise HTTPException(404, "client no encontrado")
    return c

# Variante vulnerable a CSRF vía formulario
@router.put("/{client_id}/form", dependencies=[Depends(require_login)])
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

@router.delete("/{client_id}", dependencies=[Depends(require_login)])
def delete_client(client_id: int):
    ok = client_service.delete_client(client_id)
    if not ok:
        raise HTTPException(404, "client no encontrado")
    return {"deleted": ok}

@router.get("/search")
def search(q: str):
    # Refleja el query 'q' en errores (potencial XSS si se redirige a HTML en algún cliente)
    return {"q": q, "results": client_service.search_clients(q)}

@router.get("/render")
def render():
    # Renderiza HTML sin escape -> XSS almacenado si name/notes contienen <script>
    rows = client_service.list_clients()
    html = render_clients_table(rows)
    from fastapi import Response
    return Response(content=html, media_type="text/html")
