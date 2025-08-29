from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import Base, BaseModelFieldTypes


class BaseOrderModel(Base):
    __table_args__ = {'schema': 'orders'}
    __abstract__ = True

    id: Mapped[BaseModelFieldTypes.intpk]

class OrderStatus(BaseOrderModel):
    __tablename__ = "order_status"

    name: Mapped[BaseModelFieldTypes.str_255]


class Order(BaseOrderModel):
    __tablename__ = 'orders'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("orders.order_status.id"))
    total_sum: Mapped[float] = mapped_column(nullable=True, default=0)
    is_payed: Mapped[bool]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.restaurant.id"))



class OrderFood(BaseOrderModel):
    __tablename__ = "orders_food"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.orders.id"))
    food_id: Mapped[int] = mapped_column(ForeignKey("menu.food.id"))

class OrderFoodSize(BaseOrderModel):
    __tablename__ = "orders_food_size"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.orders.id"))
    food_size_id: Mapped[int] = mapped_column(ForeignKey("menu.food_size.id"))

class OrderModifierOption(BaseOrderModel):
    __tablename__ = "orders_modifier_option"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.orders.id"))
    modifier_option_id: Mapped[int] = mapped_column(ForeignKey("menu.modifier_option.id"))


