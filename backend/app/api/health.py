from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health_status() -> dict[str, str]:
    """Report that the API process is available."""
    return {"status": "ok"}
