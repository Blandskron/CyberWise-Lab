# FastAPI Vulnerable Lab (for education only)

**⚠️ ADVERTENCIA**: Este código es intencionalmente **inseguro**. No lo despliegues en internet ni en redes de producción.
Úsalo solo en entornos locales de laboratorio.

## Objetivo
Laboratorio con vulnerabilidades comunes:
- CORS permisivo y sin protección CSRF (cookies de sesión sin tokens)
- XSS almacenado y reflejado (renderizado HTML sin sanitizar)
- Inyecciones SQL usando concatenación de strings
- Errores 500 "raros" (chaos middleware) y endpoints que filtran mensajes internos

## Requisitos
- Python 3.10+
- pip

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución
```bash
export CHAOS_RATE=0.1  # 10% de peticiones fallan con 500, opcional
uvicorn app.main:app --reload --port 8000
```
Luego abre: http://127.0.0.1:8000/docs y http://127.0.0.1:8000/redoc

## Endpoints clave
- `POST /auth/login` (inicia sesión y guarda cookie de sesión **sin CSRF**)
- `GET /clients` `POST /clients` `GET /clients/{id}` `PUT /clients/{id}` `DELETE /clients/{id}`
- `POST /clients/form` y `PUT /clients/{id}/form` (versiones `application/x-www-form-urlencoded` con riesgo CSRF)
- `GET /clients/search?q=...` (**SQLi** usando concatenación)
- `GET /clients/render` (**XSS** almacenado al renderizar HTML sin sanitizar)
- `GET /debug/random-500` y `GET /debug/echo?text=...` (500 inducido y XSS reflejado)
- `GET /health`

**Nota**: Para demostrar CSRF, inicia sesión (`/auth/login`) y luego, desde otro origen, realiza solicitudes con `credentials: 'include'` o via formularios HTML (`/clients/form`).

## Reset rápido de DB
Si deseas resetear la base SQLite, elimina el archivo `app/data/lab.db` y reinicia.
