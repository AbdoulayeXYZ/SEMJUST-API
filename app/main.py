from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import make_asgi_app

from app.core.config import settings

app = FastAPI(
    title="SEMJUST API",
    description="API d'Optimisation Équitable de la Distribution des Semences au Sénégal",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Configuration CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Middleware de sécurité
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # À configurer en production
)

# Métriques Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API SEMJUST",
        "version": "1.0.0",
        "documentation": f"{settings.API_V1_STR}/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# Import et inclusion des routers
from app.api.v1 import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 