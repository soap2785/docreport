from fastapi import APIRouter

from api.v1.request import routers as request_router


# router = FastAPI(versio="1.0")
router = APIRouter(prefix="/api/v1")
router.include_router(request_router.router)
