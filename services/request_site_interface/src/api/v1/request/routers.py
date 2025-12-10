from fastapi import APIRouter

from .views import router as request_router

router = APIRouter(tags=["Request"])

router.include_router(request_router)
