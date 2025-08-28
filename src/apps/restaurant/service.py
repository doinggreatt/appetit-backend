from sqlalchemy.ext.asyncio import AsyncSession

from .models import Restaurant
from .schemas import WriteSingleRestaurantSchema

async def create(*, db_sess: AsyncSession, rstrnt_data: WriteSingleRestaurantSchema) -> Restaurant:
    rstrnt = Restaurant(**rstrnt_data.model_dump())

    db_sess.add(rstrnt)

    await db_sess.commit()
    return rstrnt

