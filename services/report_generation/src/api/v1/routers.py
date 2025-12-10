from fastapi import APIRouter

from api.v1.generating import routers as report_generation_router


# router = FastAPI(versio="1.0")
router = APIRouter(prefix="/api/v1")
router.include_router(report_generation_router.router)
