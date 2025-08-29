from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request

from config import SessionDep
from sqlalchemy import delete

from .models import Food, FoodType, ModifierCategory, ModifierOption, Menu
from .schemas import WriteSingleFoodSchema, WriteModifierCategorySchema, WriteModifierOptionSchema, WriteFoodTypeSchema, WriteSingleMenuSchema
from .schemas import ReadModifierCategorySchema, ReadFoodTypeSchema, ReadSingleMenuSchema, ReadSingleFoodSchema
from .service import create_food_service, create_modifier_category_service, create_modifier_option_service, create_food_type_service, create_menu_service
from .service import get_modifier_category_service, get_modifier_options_service, get_food_type_service, get_menu_service, get_image_url_by_id_service
from .service import upload_file_by_id_service

common_router = APIRouter(tags=["Food"])
admin_router = APIRouter(tags=["Food - admin"])


# =============== Food

@admin_router.post("", status_code=201, response_model=ReadSingleFoodSchema)
async def create_food(db_sess: SessionDep, food_data: WriteSingleFoodSchema):
    food = await create_food_service(db_sess=db_sess, food_data=food_data)
    return food

@admin_router.post("/{food_id}/upload-image")
async def upload_food_image(
        food_id:int,
        db_sess: SessionDep,
        file: UploadFile = File(...)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in {"jpg", "jpeg", "png", "webp"}:
        raise HTTPException(status_code=400, detail="Invalid file type")

    resp = await upload_file_by_id_service(db_sess=db_sess, model=Food, id=food_id, ext=ext, upload_file=file, filepath_prefix="foods",
                                    model_filepath_attr_name="image_path")

    return resp

@common_router.get("/{food_id}/image")
async def get_food_image(
        food_id: int,
        db_ses: SessionDep,
        req: Request
):
    path = await get_image_url_by_id_service(db_sess=db_ses, model=Food, id=food_id,
                                             model_filepath_attr_name="image_path")

    return {"id": food_id, "image_url": f"{req.base_url}media/foods/{path}"}


# =============== Food Type
@admin_router.post("/type", status_code=201, response_model=ReadFoodTypeSchema)
async def create_food_type(db_sess: SessionDep, food_type_data: WriteFoodTypeSchema):
    food_type = await create_food_type_service(db_sess=db_sess, food_type_data=food_type_data)
    return food_type

@common_router.get("/type", response_model=list[ReadFoodTypeSchema])
async def get_food_type(db_sess: SessionDep):
    food_type = await get_food_type_service(db_sess=db_sess)
    return food_type

@admin_router.delete("/type/{food_type_id}", status_code=204)
async def delete_food_type(food_type_id: int, db_sess: SessionDep):
    stmt = delete(FoodType).where(FoodType.id == food_type_id)
    await db_sess.execute(stmt)
    await db_sess.commit()


# ============= Modifiers

@admin_router.post("/modifiers", status_code=201)
async def create_modifier_category(db_sess: SessionDep, modifier_cat_data: WriteModifierCategorySchema):
    modifier_category = await create_modifier_category_service(db_sess=db_sess, modifier_cat_data=modifier_cat_data)
    return modifier_category


@common_router.get("/modifiers", response_model=list[ReadModifierCategorySchema])
async def get_modifier_category(db_sess: SessionDep):
    modifier_categories = await get_modifier_category_service(db_sess=db_sess)
    return modifier_categories


@admin_router.delete("/modifiers/{modifier_cat_id}", status_code=204)
async def delete_modifier_category(modifier_cat_id: int, db_sess: SessionDep):
    stmt = delete(ModifierCategory).where(ModifierCategory.id == modifier_cat_id)
    await db_sess.execute(stmt)
    await db_sess.commit()

# ============== Modifiers options

@common_router.get("/modifiers/options")
async def get_modifier_options(db_sess: SessionDep):
    modifier_options = await get_modifier_options_service(db_sess=db_sess)
    return modifier_options

@admin_router.post("/modifiers/options")
async def create_modifier_option(db_sess: SessionDep, modifier_option_data: WriteModifierOptionSchema):
    modifier_option = await create_modifier_option_service(db_sess=db_sess, modifier_option_data=modifier_option_data)
    return modifier_option

@admin_router.delete("/modifiers/{modifier_option_id}", status_code=204)
async def delete_modifier_option(modifier_option_id: int, db_sess: SessionDep):
    stmt = delete(ModifierOption).where(ModifierOption.id == modifier_option_id)
    await db_sess.execute(stmt)
    await db_sess.commit()


# ============ Menu

@admin_router.post("/menu", description="Добавить существующее блюдо в меню", response_model=ReadSingleMenuSchema)
async def create_menu(db_sess: SessionDep, menu_data: WriteSingleMenuSchema):
    menu = await create_menu_service(db_sess=db_sess, menu_data=menu_data)
    return menu


@admin_router.delete("/menu/{menu_id}", status_code=204)
async def delete_menu(menu_id: int, db_sess: SessionDep):
    stmt = delete(Menu).where(Menu.id == menu_id)
    await db_sess.execute(stmt)
    await db_sess.commit()

@common_router.get("/menu", description="Получить меню")
async def get_menu(db_sess: SessionDep):
    resp = await get_menu_service(db_sess=db_sess)
    return resp
