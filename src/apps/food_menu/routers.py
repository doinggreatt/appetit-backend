from fastapi import APIRouter, Depends
from sqlalchemy import select

from config import SessionDep
from .models import ModifierCategory
from .schemas import WriteFoodSchema, WriteModifierCategorySchema, WriteModifierOptionSchema
from .schemas import ReadModifierCategorySchema
from .service import create_food_service, create_modifier_category_service, create_modifier_option_service
from .service import get_modifier_category_service, get_modifier_options_service

router = APIRouter(prefix="/food", tags=["Food"])

@router.post("", status_code=201)
async def create_food(db_sess: SessionDep, food_data: WriteFoodSchema):
    food = await create_food_service(db_sess=db_sess, food_data=food_data)
    return food


# ============= Modifiers

@router.post("/modifiers", status_code=201)
async def create_modifier_category(db_sess: SessionDep, modifier_cat_data: WriteModifierCategorySchema):
    modifier_category = await create_modifier_category_service(db_sess=db_sess, modifier_cat_data=modifier_cat_data)
    return modifier_category


@router.get("/modifiers", response_model=list[ReadModifierCategorySchema])
async def get_modifier_category(db_sess: SessionDep):
    modifier_categories = await get_modifier_category_service(db_sess=db_sess)
    return modifier_categories


# ============== Modifiers options

@router.get("/modifiers/options")
async def get_modifier_options(db_sess: SessionDep):
    modifier_options = await get_modifier_options_service(db_sess=db_sess)
    return modifier_options

@router.post("/modifiers/options")
async def create_modifier_option(db_sess: SessionDep, modifier_option_data: WriteModifierOptionSchema):
    modifier_option = await create_modifier_option_service(db_sess=db_sess, modifier_option_data=modifier_option_data)
    return modifier_option