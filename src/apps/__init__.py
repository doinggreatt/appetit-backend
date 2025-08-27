from fastapi import APIRouter

from .users import router as users_router
from .food_menu import admin_router as food_admin_router, common_router as food_common_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users_router)
api_router.include_router(food_admin_router, prefix="/food")
api_router.include_router(food_common_router, prefix="/food")
