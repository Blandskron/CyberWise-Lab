# Semilla rápida de datos (incluye payload con HTML para observar XSS en /clients/render)
from app.repositories.client_repository import create_client

create_client("Alice", "alice@example.com", "Hello <b>World</b>")
create_client("Bob", "bob@example.com", "<script>alert('seed')</script>")
print("Seed OK")
