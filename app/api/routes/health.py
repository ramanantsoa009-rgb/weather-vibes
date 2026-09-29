from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> Dict[str, str]:
    """Sonde de vie pour Kubernetes (liveness / readiness)."""
    return {"status": "ok"}
