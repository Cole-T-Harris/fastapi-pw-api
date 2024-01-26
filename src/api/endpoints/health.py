from fastapi import APIRouter

router = APIRouter()
# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "ok"}
