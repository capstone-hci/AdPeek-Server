from fastapi import APIRouter
from app.api.routes.gaze import router as gaze_router
from app.api.routes.session import router as session_router
from app.api.routes.result import router as result_router

router = APIRouter()
router.include_router(gaze_router)
router.include_router(session_router)
router.include_router(result_router)