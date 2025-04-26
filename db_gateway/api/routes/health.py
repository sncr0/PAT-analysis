from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
def healthz_check():
    return {"status": "ok 2"}


@router.get("/health")
def health_check():
    return {"status": "ok 2"}
