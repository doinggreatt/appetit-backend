from datetime import datetime


from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.sqltypes import LargeBinary
from argon2.exceptions import VerifyMismatchError

from config import Base, BaseModelFieldTypes
from config import get_module_logger

from .auth_utils import hash_password, hasher

logger = get_module_logger('auth')

class BaseUserModel(Base):
    __abstract__ = True
    __table_args__ = {'schema': 'users'}

class User(BaseUserModel):
    __tablename__ = 'user'
    id: Mapped[BaseModelFieldTypes.intpk]
    email: Mapped[BaseModelFieldTypes.str_255]
    first_name: Mapped[BaseModelFieldTypes.str_255]
    last_name: Mapped[BaseModelFieldTypes.str_255]
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now()
    )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_password(self, password: str) -> None:
        """Set a new password for the user."""
        if not password:
            raise ValueError("Password cannot be empty")
        password = bytes(password, encoding='utf-8')
        self.password = hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verifies inputted password with user's password."""
        if not password:
            return False
        try:
            verify: bool = hasher.verify(self.password, password)
            return verify
        except VerifyMismatchError:
            return False