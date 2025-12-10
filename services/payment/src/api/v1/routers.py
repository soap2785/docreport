from fastapi import APIRouter

from api.v1.payment import routers as payment_router


# router = FastAPI(versio="1.0")
router = APIRouter(prefix="/api/v1")
router.include_router(payment_router.router)
