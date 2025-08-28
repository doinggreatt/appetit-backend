from sqlalchemy.orm import Mapped

from config import Base, BaseModelFieldTypes
from config import get_module_logger


class BaseRestaurantModel(Base):
    __table_args__ = {'schema': 'restaurant'}
    __abstract__ = True

    id: Mapped[BaseModelFieldTypes.intpk]


class Restaurant(BaseRestaurantModel):
    __tablename__ = 'restaurant'

    name: Mapped[BaseModelFieldTypes.str_255]
    lat: Mapped[float]
    lon: Mapped[float]
