from fastapi import Depends, Request, HTTPException
from sqlalchemy import select

from config import SessionDep
from .models import User
from .service import get_user_by
from .auth_config import authx
from .enums import UserLookupField

async def admin_role_required(req: Request, db_sess: SessionDep, token=Depends(authx.access_token_required)):
    user_id = token.sub
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.ID, value=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="not found")

    return user

