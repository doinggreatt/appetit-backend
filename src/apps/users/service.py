from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from .auth_config import authx
from .schemas import UserWriteSchema, AccessTokenLoginSchema
from .models import User
from .enums import UserLookupField

async def get_user_by(
        *,
        db_sess: AsyncSession,
        field: UserLookupField,
        value: str | int
) -> User | None:
    stmt = None

    match field:
        case UserLookupField.EMAIL:
            stmt = select(User).where(User.email == value)
        case UserLookupField.ID:
            stmt = select(User).where(User.id == int(value))
        case UserLookupField.TOKEN:
            sub = authx.verify_token(token=value)
            stmt = select(User).where(User.id == int(sub))
        case _:
            raise ValueError(f"unsupported lookup: {field}")

    res = await db_sess.execute(stmt)
    res = res.scalar_one_or_none()

    return res


async def create(*, db_sess: AsyncSession, user_data: UserWriteSchema) -> tuple[dict[str, str], int]:
    """Creates User object"""
    if await get_user_by(db_sess=db_sess,
                         field=UserLookupField.EMAIL,
                         value=user_data.email):

        raise HTTPException(
            status_code=400,
            detail="this username is already taken"
        )

    try:
        new_user = User(**user_data.model_dump(exclude={"password", "password_2"}))
        new_user.set_password(user_data.password)

        db_sess.add(new_user)
        await db_sess.commit()
        await db_sess.refresh(new_user)

        return new_user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def authorize(*, db_sess: AsyncSession, login_data: AccessTokenLoginSchema) -> dict[str, str,]:
    """Authorizes user"""
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.EMAIL, value=login_data.email)

    if user and user.verify_password(login_data.password):
        access_token = authx.create_access_token(uid=str(user.id))
        return {'access_token': access_token}

    raise HTTPException(status_code=401, detail="wrong credentials")
