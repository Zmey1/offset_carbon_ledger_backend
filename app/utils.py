import hashlib
import re

def _canon_text(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def deterministic_id(project_name: str, registry: str, vintage: int, quantity: int) -> str:
    "Use SHA-256 to create a deterministic ID for a credit record (max length of 16)."
    key = f"{_canon_text(project_name)}|{_canon_text(registry)}|{int(vintage)}|{int(quantity)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
