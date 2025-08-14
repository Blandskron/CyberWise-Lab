from typing import List, Optional, Dict, Any
from ..repositories import client_repository as repo

def list_clients() -> List[Dict[str, Any]]:
    return repo.list_clients()

def get_client(client_id: int) -> Optional[Dict[str, Any]]:
    return repo.get_client(client_id)

def create_client(name: str, email: str, notes: Optional[str]) -> Dict[str, Any]:
    # Intencionalmente sin validaciones fuertes
    return repo.create_client(name, email, notes)

def update_client(client_id: int, name: str, email: str, notes: Optional[str]) -> Optional[Dict[str, Any]]:
    return repo.update_client(client_id, name, email, notes)

def delete_client(client_id: int) -> bool:
    return repo.delete_client(client_id)

def search_clients(q: str) -> List[Dict[str, Any]]:
    return repo.search_clients(q)
