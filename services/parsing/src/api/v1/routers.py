from fastapi import APIRouter

from api.v1.parsing import routers as parsing_router


# router = FastAPI(versio="1.0")
router = APIRouter(prefix="/api/v1")
router.include_router(parsing_router.router)
