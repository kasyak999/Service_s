from fastapi import APIRouter
from .endpoints import home_router, page_router, auth_router


web_router = APIRouter(tags=['Веб версия'])
web_router.include_router(home_router)
