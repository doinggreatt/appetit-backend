import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_module_logger
from apps.contrib import InternalError
from sqlalchemy.orm import selectinload

from .schemas import WriteSingleFoodSchema, WriteModifierCategorySchema, ReadModifierCategoryOptionSchema, \
    ReadSingleModifierOptionSchema, WriteModifierOptionSchema, WriteFoodTypeSchema, WriteSingleMenuSchema, \
    ReadSingleFoodSchema, ReadSingleFoodSizeSchema, ReadAllMenu
from .models import Food, FoodSize, FoodType, FoodModifierOption, ModifierCategory, ModifierOption, Menu


logger: logging.Logger = get_module_logger(__name__)


async def _create(*, db_sess: AsyncSession, model_dump_data: dict[str, Any], model: Any) -> Any:
    new_obj = model(**model_dump_data)

    db_sess.add(new_obj)
    await db_sess.commit()
    await db_sess.flush()

    return new_obj

async def _get_food_detail_by_food_id(*, db_sess: AsyncSession, food_id: int) -> ReadSingleFoodSchema:

    try:


        food = await db_sess.execute(select(Food).where(Food.id == food_id))
        food = food.scalars().one_or_none()

        food_sizes = await db_sess.execute(
            select(FoodSize).where(FoodSize.parent_id == food.id)
        )

        food_sizes = food_sizes.scalars().all()

        food_sizes = [ReadSingleFoodSizeSchema(
            id=food_size.id,
            name=food_size.name,
            is_new=food_size.is_new,
            price=food_size.price
        ) for food_size in food_sizes]

        food_modifier_options = await db_sess.execute(
            select(FoodModifierOption)
            .where(FoodModifierOption.food_id == food.id)
            .options(selectinload(FoodModifierOption.option).selectinload(ModifierOption.modifier_category))
        )

        food_modifier_options = food_modifier_options.scalars().all()

        output_food_modifiers = list()

        for food_modifier_option in food_modifier_options:
            modifier_option = ReadSingleModifierOptionSchema(
                id=food_modifier_option.option.id,
                name=food_modifier_option.option.name,
                price=food_modifier_option.option.price

            )

            if food_modifier_option.option.modifier_category_id not in [item["modifier_cat_id"] for item in output_food_modifiers]:
                output_food_modifiers.append(
                    {
                        "modifier_cat_id": food_modifier_option.option.modifier_category_id,
                        "modifier_cat_name": food_modifier_option.option.modifier_category.name,
                        "modifier_options": [modifier_option]
                    }
                )
            else:

                output_food_modifier_item = next((_ for _ in output_food_modifiers if _["modifier_cat_id"]  == food_modifier_option.option.modifier_category_id), None)

                assert output_food_modifier_item

                output_food_modifier_item["modifier_options"].append(
                    modifier_option
                )

        resp = ReadSingleFoodSchema(
            name=food.name,
            description=food.description,
            food_sizes=food_sizes,
            food_modifiers=output_food_modifiers,
            food_type_id=food.food_type.id,
            food_type_name=food.food_type.name,
        )

        return resp

    except Exception as e:
        raise InternalError(e, module_name=__name__)




async def create_food_service(*, db_sess: AsyncSession, food_data: WriteSingleFoodSchema):


    try:
        new_food_obj = Food(**food_data.model_dump(exclude=['possible_food_modifiers', 'food_sizes']))
        db_sess.add(new_food_obj)
        await db_sess.flush()

        for food_size_data in food_data.food_sizes:
            new_food_size_obj = FoodSize(
                name=food_size_data.name,
                parent_id=new_food_obj.id,
                is_new=food_size_data.is_new,
                price=food_size_data.price
            )

            db_sess.add(new_food_size_obj)


        for food_modifier_id in food_data.possible_food_modifiers:
            new_food_modifier_option_obj = FoodModifierOption(
                food_id=new_food_obj.id,
                modifier_option_id=food_modifier_id
            )

            db_sess.add(new_food_modifier_option_obj)

        await db_sess.flush()

        resp = await _get_food_detail_by_food_id(db_sess=db_sess, food_id=new_food_obj.id)

        return resp

    except Exception as e:
        raise InternalError(e, module_name=__name__)



async def create_modifier_category_service(*, db_sess: AsyncSession, modifier_cat_data: WriteModifierCategorySchema):
    try:
        modifier_category = ModifierCategory(**modifier_cat_data.model_dump())

        db_sess.add(modifier_category)
        await db_sess.commit()

        return modifier_category

    except Exception as e:
        raise InternalError(e, module_name=__name__)


async def get_modifier_category_service(*, db_sess: AsyncSession):
    try:
        stmt = select(ModifierCategory)
        res = await db_sess.execute(stmt)

        return res.scalars().all()

    except Exception as e:
        raise InternalError(e, module_name=__name__)

async def get_modifier_options_service(*, db_sess: AsyncSession):

    modifier_cats = set()

    output: list[ReadModifierCategoryOptionSchema] = list()

    try:
        stmt = select(ModifierOption)
        res = await db_sess.execute(stmt)
        modifier_options = res.scalars().all()
        if len(modifier_options) > 0:

            for modifier_option in modifier_options:

                if modifier_option.modifier_category_id not in modifier_cats:
                    res = await db_sess.execute(select(ModifierCategory).where(ModifierCategory.id == modifier_option.modifier_category_id))
                    modifier_cat = res.scalars().one_or_none()

                    modifier_cats.add(modifier_cat)
                    output.append(
                        ReadModifierCategoryOptionSchema(
                            modifier_cat_id=modifier_cat.id,
                            modifier_cat_name=modifier_cat.name,
                        )
                    )

                for _ in output:
                    if _.modifier_cat_id == modifier_option.modifier_category_id:
                        _.modifier_options.append(
                            ReadSingleModifierOptionSchema(
                                id=modifier_option.id,
                                name=modifier_option.name,
                                price=modifier_option.price
                            )
                        )


        return output

    except Exception as e:
        raise InternalError(e, module_name=__name__)

async def create_modifier_option_service(*, db_sess: AsyncSession, modifier_option_data: WriteModifierOptionSchema):
    try:
        modifier_option = ModifierOption(**modifier_option_data.model_dump())

        db_sess.add(modifier_option)

        await db_sess.commit()
        await db_sess.flush()

        return modifier_option

    except Exception as e:
        raise InternalError(e, module_name=__name__)


async def create_food_type_service(*, db_sess: AsyncSession, food_type_data: WriteFoodTypeSchema):
    try:
        food_type = await _create(db_sess=db_sess, model_dump_data=food_type_data.model_dump(), model=FoodType)
        return food_type

    except Exception as e:
        raise InternalError(e, module_name=__name__)


async def get_food_type_service(*, db_sess: AsyncSession):
    try:
        stmt = select(FoodType)
        res = await db_sess.execute(stmt)

        food_types = res.scalars().all()

        return food_types

    except Exception as e:
        raise InternalError(e, module_name=__name__)

async def create_menu_service(*, db_sess: AsyncSession, menu_data: WriteSingleMenuSchema):
    try:
        menu = Menu(**menu_data.model_dump())

        db_sess.add(menu)
        await db_sess.commit()

        await db_sess.flush()

        return menu
    except Exception as e:
        raise InternalError(e, module_name=__name__)


async def get_menu_service(*, db_sess: AsyncSession):
    try:
        menu = await db_sess.execute(select(Menu))
        menu = menu.scalars().all()

        output = list()

        for _menu in menu:
            food_id = _menu.food_id

            food_detail = await _get_food_detail_by_food_id(db_sess=db_sess, food_id=food_id)

            if food_detail.food_type_id not in [item["food_type_id"] for item in output]:
                output.append(
                    {
                        "food_type_id": food_detail.food_type_id,
                        "food_type_name": food_detail.food_type_name,
                        "foods": [food_detail]
                    }
                )
            else:

                output_item = next((_ for _ in output if _["food_type_id"]  == food_detail.food_type_id), None)
                output_item["foods"].append(food_detail)

            output = [ReadAllMenu(
                food_type_name=item["food_type_name"],
                food_type_id=item["food_type_id"],
                foods=item["foods"]
                ) for item in output]

        return output








    except Exception as e:
        raise InternalError(e, module_name=__name__)