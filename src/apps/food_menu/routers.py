from fastapi import APIRouter, Depends

from config import SessionDep
from .schemas import WriteFoodSchema, WriteModifierCategorySchema, WriteModifierOptionSchema, WriteFoodTypeSchema, WriteSingleMenuSchema
from .schemas import ReadModifierCategorySchema, ReadFoodTypeSchema, ReadSingleMenuSchema
from .service import create_food_service, create_modifier_category_service, create_modifier_option_service, create_food_type_service, create_menu_service
from .service import get_modifier_category_service, get_modifier_options_service, get_food_type_service

common_router = APIRouter(tags=["Food"])
admin_router = APIRouter(tags=["Food - admin"])


# =============== Food

@common_router.post("", status_code=201)
async def create_food(db_sess: SessionDep, food_data: WriteFoodSchema):
    food = await create_food_service(db_sess=db_sess, food_data=food_data)
    return food


# =============== Food Type
@admin_router.post("/type", status_code=201, response_model=ReadFoodTypeSchema)
async def create_food_type(db_sess: SessionDep, food_type_data: WriteFoodTypeSchema):
    food_type = await create_food_type_service(db_sess=db_sess, food_type_data=food_type_data)
    return food_type

@common_router.get("/type", response_model=list[ReadFoodTypeSchema])
async def get_food_type(db_sess: SessionDep):
    food_type = await get_food_type_service(db_sess=db_sess)
    return food_type

# ============= Modifiers

@admin_router.post("/modifiers", status_code=201)
async def create_modifier_category(db_sess: SessionDep, modifier_cat_data: WriteModifierCategorySchema):
    modifier_category = await create_modifier_category_service(db_sess=db_sess, modifier_cat_data=modifier_cat_data)
    return modifier_category


@common_router.get("/modifiers", response_model=list[ReadModifierCategorySchema])
async def get_modifier_category(db_sess: SessionDep):
    modifier_categories = await get_modifier_category_service(db_sess=db_sess)
    return modifier_categories


# ============== Modifiers options

@common_router.get("/modifiers/options")
async def get_modifier_options(db_sess: SessionDep):
    modifier_options = await get_modifier_options_service(db_sess=db_sess)
    return modifier_options

@admin_router.post("/modifiers/options")
async def create_modifier_option(db_sess: SessionDep, modifier_option_data: WriteModifierOptionSchema):
    modifier_option = await create_modifier_option_service(db_sess=db_sess, modifier_option_data=modifier_option_data)
    return modifier_option

# ============ Menu

@admin_router.post("/menu", description="Добавить существующее блюдо в меню", response_model=ReadSingleMenuSchema)
async def create_menu(db_sess: SessionDep, menu_data: WriteSingleMenuSchema):
    menu = await create_menu_service(db_sess=db_sess, menu_data=menu_data)
    return menu
