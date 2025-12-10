from fastapi import APIRouter

from .views import router as parsing_router

router = APIRouter(tags=["Parsing"])

router.include_router(parsing_router)
