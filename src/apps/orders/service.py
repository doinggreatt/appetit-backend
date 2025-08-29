from typing import Iterable, Any

from fastapi import HTTPException, Request
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Order, OrderStatus, OrderFood, OrderFoodSize, OrderModifierOption
from apps.food_menu.models import ModifierOption, FoodSize
from apps.users.enums import UserLookupField
from apps.users.service import get_user_by
from .schemas import WriteSingleOrderSchema, ReadSingleOrderSchema


async def _count_total_sum(*, db_sess: AsyncSession, total_sum: int, model: Any, ids: list) -> int:


    stmt = select(model).where(model.id.in_(ids ))
    res = await db_sess.execute(stmt)
    res = res.scalars().all()

    for _ in res:
        total_sum += _.price

    return total_sum


async def _get_pending_status_id(*, db_sess: AsyncSession) -> int:
    stmt = select(OrderStatus).where(OrderStatus.name == "pending")

    res = await db_sess.execute(stmt)

    res = res.scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=500, detail="No pending status is created")
    return res.id

async def create(*, db_sess: AsyncSession, order_data: WriteSingleOrderSchema, req: Request):
    status_id = await _get_pending_status_id(db_sess=db_sess)
    total_sum = 0
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.REQUEST, value=req)
    order = Order(status_id=status_id, is_payed=order_data.is_payed, user_id=user.id, restaurant_id=order_data.restaurant_id)
    db_sess.add(order)
    await db_sess.commit()

    for food_id in order_data.food_ids:
        new_order_food_obj = OrderFood(order_id=order.id, food_id=food_id)
        db_sess.add(new_order_food_obj)

    for food_size_id in order_data.food_size_ids:
        new_order_food_size_obj = OrderFoodSize(order_id=order.id, food_size_id=food_size_id)
        db_sess.add(new_order_food_size_obj)

    total_sum = await _count_total_sum(db_sess=db_sess, total_sum=total_sum, model=FoodSize, ids=order_data.food_size_ids)
    total_sum = await _count_total_sum(db_sess=db_sess, total_sum=total_sum, model=ModifierOption, ids=order_data.modifier_option_ids)

    order.total_sum = total_sum

    db_sess.add(order)
    await db_sess.commit()

    out = ReadSingleOrderSchema(
        id=order.id,
    )

    return out
