import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_module_logger
from apps.common import InternalError
from .schemas import WriteFoodSchema, WriteModifierCategorySchema, ReadModifierCategoryOptionSchema, \
    ReadSingleModifierOptionSchema, WriteModifierOptionSchema, WriteFoodTypeSchema
from .models import Food, FoodSize, FoodType, FoodModifierOption, ModifierCategory, ModifierOption


logger: logging.Logger = get_module_logger(__name__)


async def _create(*, db_sess: AsyncSession, model_dump_data: dict[str, Any], model: Any) -> Any:
    new_obj = model(**model_dump_data)

    db_sess.add(new_obj)
    await db_sess.commit()
    await db_sess.flush()

    return new_obj



async def create_food_service(*, db_sess: AsyncSession, food_data: WriteFoodSchema):

    try:
        new_food_obj = Food(**food_data.model_dump(exclude=['possible_food_modifiers', 'food_sizes']))
        db_sess.add(new_food_obj)
        await db_sess.commit()
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

        return new_food_obj

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
        raise InternalError(e, __name__)

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
    stmt = select(FoodType)
    res = await db_sess.execute(stmt)

    food_types = res.scalars().all()

    return food_types