from fastapi import APIRouter

router = APIRouter()
# Health check endpoint
@router.get("/")
async def health_check():
    return {"status": "ok"}
