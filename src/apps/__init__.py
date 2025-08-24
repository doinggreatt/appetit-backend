from fastapi import APIRouter

from .users import router as users_router
from .food_menu import router as food_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users_router)
api_router.include_router(food_router)
