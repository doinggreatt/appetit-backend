from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import Base, BaseModelFieldTypes


class BaseOrderModel(Base):
    __table_args__ = {'schema': 'orders'}
    __abstract__ = True

    id: Mapped[BaseModelFieldTypes.intpk]


class Order(BaseOrderModel):
    __tablename__ = 'orders'

