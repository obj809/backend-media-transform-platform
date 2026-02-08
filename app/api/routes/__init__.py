from fastapi import APIRouter

from .root import router as root_router
from .health import router as health_router
from .upload import router as upload_router

router = APIRouter()

router.include_router(root_router)
router.include_router(health_router)
router.include_router(upload_router)
