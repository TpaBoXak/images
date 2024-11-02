from fastapi import APIRouter

from config import settings


api_router = APIRouter(prefix=settings.api.prefix)
template_router = APIRouter()

from .auth import router as auth_router
api_router.include_router(auth_router)


from .images import router as images_router
api_router.include_router(images_router)


from .html_files import router as templates_router
template_router.include_router(templates_router)
