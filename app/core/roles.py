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

def get_system_prompt(role_id: str) -> str | None:
    role = get_role(role_id)
    if not role:
        return None
    sp = (role.get("system_prompt") or "").strip()
    return sp or None

def list_roles() -> list[dict]:
    data = _load_all()
    out = []
    for k, v in data.items():
        sp = (v.get("system_prompt") or "")
        out.append({
            "id": k,
            "name": v.get("name"),
            "has_prompt": bool(sp),
            "prompt_len": len(sp),
        })
    return out

def reload_roles() -> int:
    # invalida el caché del lru_cache y recarga
    _load_all.cache_clear()           # type: ignore[attr-defined]
    data = _load_all()
    return len(data)