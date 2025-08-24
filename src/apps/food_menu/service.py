import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from config import get_module_logger
from .schemas import WriteFoodSchema
from .models import Food, FoodSize, FoodModifierOption


logger: logging.Logger = get_module_logger(__name__)


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
        logger.error(f"Error when trying to create new food: {e}")
        raise HTTPException(status_code=500, detail="Error when trying to create data. Try to contact administrator.")







