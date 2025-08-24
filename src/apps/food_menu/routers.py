from fastapi import APIRouter, Depends

from config import SessionDep
from .schemas import WriteFoodSchema
from .service import create_food_service

router = APIRouter(prefix="/food")

@router.post("", status_code=201)
async def create_food(db_sess: SessionDep, food_data: WriteFoodSchema):
    food = await create_food_service(db_sess=db_sess, food_data=food_data)
    return food

