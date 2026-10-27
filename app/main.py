from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .api.routes import (
    auth_router,
    candidate_router,
    health_router,
    vote_router,
    voter_router,
)
from .services import database as _databaseService


@asynccontextmanager
async def lifespan(app: FastAPI):
    _databaseService.create_database()
    yield


# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Sistema de Votaciones",
    description="API REST para gestionar una votación: registro de votantes y candidatos, emisión de votos (uno por votante) y estadísticas de resultados. Un votante no puede ser candidato, ni un candidato votante.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Al momento de visitar la raiz del proyecto, redirigimos a /docs (ruta donde está la documentación automática de FastAPI)
@app.get("/", include_in_schema=False)
async def root():
    """Redirige a la documentación automática."""
    return RedirectResponse(url="/docs")


router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(voter_router, prefix="/voters", tags=["Voters"])
router.include_router(candidate_router, prefix="/candidates", tags=["Candidates"])
router.include_router(vote_router, prefix="/votes", tags=["Votes"])

app.include_router(router)
