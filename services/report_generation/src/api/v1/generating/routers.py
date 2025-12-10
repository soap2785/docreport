from fastapi import APIRouter

from .views import router as report_generation_router

router = APIRouter(tags=["Generating"])

router.include_router(report_generation_router)
