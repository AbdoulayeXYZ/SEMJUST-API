from fastapi import APIRouter

from app.api.v1.endpoints import regions, departements, allocations, auth, users, notifications, optimization

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(regions.router, prefix="/regions", tags=["regions"])
api_router.include_router(departements.router, prefix="/departements", tags=["departements"])
api_router.include_router(allocations.router, prefix="/allocations", tags=["allocations"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(optimization.router, prefix="/optimization", tags=["optimization"]) 