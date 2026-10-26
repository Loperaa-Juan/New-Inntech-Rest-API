from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from .api.routes import health_router

# Inicilizamos la aplicación FastAPI
app = FastAPI(
    title="Sistema de Votaciones",
    description="API para un sistema de votaciones que permite a los usuarios crear encuestas, votar y ver resultados.",
    version="1.0.0",
)


# Al momento de visitar la raiz del proyecto, redirigimos a /docs (ruta donde está la documentación automática de FastAPI)
@app.get("/", include_in_schema=False)
async def root():
    """Redirect to the automatic documentation."""
    return RedirectResponse(url="/docs")


router = APIRouter(prefix="/api")

router.include_router(health_router)

app.include_router(router)
