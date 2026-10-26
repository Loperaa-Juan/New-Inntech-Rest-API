from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from .api.routes import health_router, voter_router
from .services import database as _databaseService


@asynccontextmanager
async def lifespan(app: FastAPI):
    _databaseService.create_database()
    yield


# Inicilizamos la aplicación FastAPI
app = FastAPI(
    title="Sistema de Votaciones",
    description="API para un sistema de votaciones que permite a los usuarios crear encuestas, votar y ver resultados.",
    version="1.0.0",
    lifespan=lifespan,
)


# Al momento de visitar la raiz del proyecto, redirigimos a /docs (ruta donde está la documentación automática de FastAPI)
@app.get("/", include_in_schema=False)
async def root():
    """Redirige a la documentación automática."""
    return RedirectResponse(url="/docs")


router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(voter_router, prefix="/voters", tags=["Voters"])

app.include_router(router)
