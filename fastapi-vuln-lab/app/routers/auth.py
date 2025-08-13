from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginBody(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(body: LoginBody, response: Response):
    # Contraseña ignorada: autenticación débil intencional
    # Guardamos un "session" cookie sin protección CSRF ni expiración correcta
    response.set_cookie(key="session", value=body.username, httponly=True, samesite="lax")
    # Mensaje con eco del usuario (no sanitizado si se renderiza como HTML en algún cliente)
    return {"message": f"Bienvenido {body.username}", "user": body.username}
