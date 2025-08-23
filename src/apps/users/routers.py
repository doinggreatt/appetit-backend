from fastapi import APIRouter, Depends
from sqlalchemy import select

from config import SessionDep
from .models import User
from .schemas import UserWriteSchema, UserReadSchema, AccessTokenLoginSchema
from .service import create, authorize
from .depends import admin_role_required

router = APIRouter(prefix="/users")

@router.get("", response_model=list[UserReadSchema], dependencies=[Depends(admin_role_required)])
async def list_users(db_sess: SessionDep):
    stmt = select(User)
    res = await db_sess.execute(stmt)
    users = res.scalars().all()

    return users

@router.post("", response_model=UserReadSchema)
async def create_user(db_sess: SessionDep, user_data: UserWriteSchema):
    user = await create(db_sess=db_sess, user_data=user_data)

    return user

@router.post("/authorize")
async def authorize_user(db_sess: SessionDep, login_data: AccessTokenLoginSchema):
    access_token = await authorize(db_sess=db_sess, login_data=login_data)

    return access_token