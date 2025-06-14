from app.api.dev.endpoints.superuser import router as superuser_router
from fastapi import APIRouter

routers = APIRouter()
routers.include_router(superuser_router)
