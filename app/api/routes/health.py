from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health", tags=["Health Check"], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Endpoint Health check para verificar que la API esté en funcionamiento.
    """
    return {"status": "healthy"}
