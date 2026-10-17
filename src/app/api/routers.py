from fastapi import APIRouter
from .endpoints import user_router


api_router = APIRouter(prefix='/api')
# api_router.include_router(systems_router)
api_router.include_router(user_router)
# api_router.include_router(account_router)
