from fastapi import APIRouter
from sqlalchemy import select

from config import SessionDep
from .models import Restaurant
from .service import create
from .schemas import WriteSingleRestaurantSchema
from .schemas import ReadSingleRestaurantSchema



admin_router = APIRouter(tags=["Restaurant - admin"])
common_router = APIRouter(tags=["Restaurant"])


@admin_router.post("", description="Создать новый ресторан", response_model=ReadSingleRestaurantSchema)
async def create_rstrnt(db_sess: SessionDep, rstrnt_data: WriteSingleRestaurantSchema):
    rstrnt = await create(db_sess=db_sess, rstrnt_data=rstrnt_data)

    return rstrnt

@common_router.get("", description="Получить список всех ресторанов", response_model=list[ReadSingleRestaurantSchema])
async def lists_rstrnts(db_sess: SessionDep):
    stmt = select(Restaurant)
    rstrnts = await db_sess.execute(stmt)
    rstrnts = rstrnts.scalars().all()

    return rstrnts
