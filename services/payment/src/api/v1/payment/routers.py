from fastapi import APIRouter

from .views import router as payment_router

router = APIRouter(tags=["Payment"])

router.include_router(payment_router)
