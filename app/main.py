from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import make_asgi_app

from app.core.config import settings
from app.metrics import ALLOCATION_GAUGE
import random
from fastapi import APIRouter

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

@app.post("/populate_test_data")
def populate_test_data():
    regions_departements = [
        {"region": "Dakar", "departements": [
            {"name": "Dakar", "lat": 14.6928, "lon": -17.4467},
            {"name": "Guediawaye", "lat": 14.7841, "lon": -17.4065},
            {"name": "Pikine", "lat": 14.7645, "lon": -17.3907},
            {"name": "Rufisque", "lat": 14.7156, "lon": -17.2736}
        ]},
        {"region": "Thiès", "departements": [
            {"name": "Thiès", "lat": 14.7910, "lon": -16.9256},
            {"name": "Mbour", "lat": 14.4205, "lon": -16.9644},
            {"name": "Tivaouane", "lat": 15.1500, "lon": -16.8167}
        ]},
        {"region": "Saint-Louis", "departements": [
            {"name": "Saint-Louis", "lat": 16.0179, "lon": -16.4896},
            {"name": "Dagana", "lat": 16.6092, "lon": -15.6076},
            {"name": "Podor", "lat": 16.6556, "lon": -14.9722}
        ]},
        {"region": "Kaolack", "departements": [
            {"name": "Kaolack", "lat": 14.1460, "lon": -16.0726},
            {"name": "Guinguinéo", "lat": 14.2611, "lon": -15.9500},
            {"name": "Nioro du Rip", "lat": 13.7500, "lon": -15.8000}
        ]},
        {"region": "Ziguinchor", "departements": [
            {"name": "Ziguinchor", "lat": 12.5833, "lon": -16.2719},
            {"name": "Bignona", "lat": 12.8081, "lon": -16.2264},
            {"name": "Oussouye", "lat": 12.4856, "lon": -16.5461}
        ]},
        {"region": "Fatick", "departements": [
            {"name": "Fatick", "lat": 14.3396, "lon": -16.4160},
            {"name": "Foundiougne", "lat": 14.1333, "lon": -16.4667},
            {"name": "Gossas", "lat": 14.6500, "lon": -16.0667}
        ]},
        {"region": "Kolda", "departements": [
            {"name": "Kolda", "lat": 12.8833, "lon": -14.9500},
            {"name": "Velingara", "lat": 13.1500, "lon": -14.1167},
            {"name": "Medina Yoro Foulah", "lat": 13.2167, "lon": -14.0833}
        ]},
        {"region": "Tambacounda", "departements": [
            {"name": "Tambacounda", "lat": 13.7707, "lon": -13.6673},
            {"name": "Bakel", "lat": 14.9000, "lon": -12.4667},
            {"name": "Goudiry", "lat": 14.1833, "lon": -12.8833},
            {"name": "Koumpentoum", "lat": 13.9833, "lon": -13.1167}
        ]},
        {"region": "Louga", "departements": [
            {"name": "Louga", "lat": 15.6144, "lon": -16.2244},
            {"name": "Kebemer", "lat": 15.3333, "lon": -16.4167},
            {"name": "Linguere", "lat": 15.3833, "lon": -15.1167}
        ]},
        {"region": "Matam", "departements": [
            {"name": "Matam", "lat": 15.6559, "lon": -13.2554},
            {"name": "Kanel", "lat": 15.5000, "lon": -13.1833},
            {"name": "Ranerou", "lat": 15.6333, "lon": -13.4167}
        ]},
        {"region": "Diourbel", "departements": [
            {"name": "Diourbel", "lat": 14.6556, "lon": -16.2342},
            {"name": "Bambey", "lat": 14.7000, "lon": -16.4667},
            {"name": "Mbacke", "lat": 14.9900, "lon": -15.6800}
        ]},
        {"region": "Kaffrine", "departements": [
            {"name": "Kaffrine", "lat": 14.1050, "lon": -15.5500},
            {"name": "Birkilane", "lat": 14.2833, "lon": -15.4167},
            {"name": "Koungheul", "lat": 13.9833, "lon": -14.8167},
            {"name": "Malem Hodar", "lat": 14.1833, "lon": -15.1167}
        ]},
        {"region": "Sédhiou", "departements": [
            {"name": "Sedhiou", "lat": 12.7081, "lon": -15.5569},
            {"name": "Bounkiling", "lat": 12.8000, "lon": -15.2333},
            {"name": "Goudomp", "lat": 12.5167, "lon": -15.3667}
        ]},
        {"region": "Kédougou", "departements": [
            {"name": "Kedougou", "lat": 12.5556, "lon": -12.1744},
            {"name": "Salemata", "lat": 12.7000, "lon": -12.7000},
            {"name": "Saraya", "lat": 12.8833, "lon": -12.5333}
        ]}
    ]

    types_semence = ["mil", "maïs", "arachide", "riz"]
    allocations = []
    for region in regions_departements:
        for dep in region["departements"]:
            for type_semence in types_semence:
                quantite = random.randint(50, 500)
                ALLOCATION_GAUGE.labels(
                    region=region["region"],
                    departement=dep["name"],
                    lat=str(dep["lat"]),
                    lon=str(dep["lon"]),
                    type_semence=type_semence
                ).set(quantite)
                allocations.append({
                    "region": region["region"],
                    "departement": dep["name"],
                    "lat": dep["lat"],
                    "lon": dep["lon"],
                    "type_semence": type_semence,
                    "quantite": quantite
                })
    return {"message": "Données de test injectées", "allocations": allocations}

@app.post("/populate_postgres_data")
def populate_postgres_data():
    from app.metrics import populate_postgres_test_data
    populate_postgres_test_data()
    return {"message": "Données PostgreSQL injectées avec succès"}

# Import et inclusion des routers
from app.api.v1 import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)