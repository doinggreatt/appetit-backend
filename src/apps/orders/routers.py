from fastapi import APIRouter, Request

from config import SessionDep
from .schemas import WriteSingleOrderSchema
from .service import create

common_router = APIRouter(tags=["Orders"])
admin_router = APIRouter(tags=["Orders - admin"])

@common_router.post("", description="Создать новый заказ")
async def create_order(db_sess: SessionDep, order_data: WriteSingleOrderSchema, req: Request):
    order = await create(db_sess=db_sess, order_data=order_data, req=req)
