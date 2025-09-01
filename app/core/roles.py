import json
from pathlib import Path
from functools import lru_cache

ROLES_PATH = Path(__file__).resolve().parent.parent / "config" / "roles.json"

@lru_cache(maxsize=1)
def _load_all() -> dict:
    if not ROLES_PATH.exists():
        return {}
    with ROLES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_role(role_id: str) -> dict | None:
    return _load_all().get(role_id)