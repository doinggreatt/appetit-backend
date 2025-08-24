from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import Base, BaseModelFieldTypes
from config import get_module_logger


class BaseMenuModel(Base):
    __abstract__ = True
    __table_args__ = {'schema': 'menu'}

    id: Mapped[BaseModelFieldTypes.intpk]

class Menu(BaseMenuModel):
    __tablename__ = "menu"

    name: Mapped[BaseModelFieldTypes.str_255]
    priority_level: Mapped[int]  = mapped_column(nullable=True)
    priority_name: Mapped[str]


class FoodType(BaseMenuModel):
    __tablename__ = "food_type"

    name: Mapped[BaseModelFieldTypes.str_255]

    foods: Mapped["Food"] = relationship(back_populates="food_type")

class Food(BaseMenuModel):
    __tablename__ = "food"

    name: Mapped[BaseModelFieldTypes.str_255]
    type_id: Mapped[int] = mapped_column(ForeignKey("food_type.id"))

    food_type: Mapped["FoodType"] = relationship(back_populates="foods")
    sizes: Mapped["FoodSize"] = relationship(back_populates="parent_food")

class FoodSize(BaseMenuModel):
    __tablename__ = "food_size"

    name: Mapped[BaseModelFieldTypes.str_255]
    parent_id: Mapped[int] = mapped_column(ForeignKey("food.id"))
    is_new: Mapped[bool] = mapped_column(default=False)
    price: Mapped[float]

    parent_food = relationship(back_populates="sizes")




class FoodModifierOptions(BaseMenuModel):
    __tablename__ = "food_modifier_options"

    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"))
    modifier_option_id: Mapped[int] = mapped_column(ForeignKey("modifier_option.id"))
    
    food: Mapped["Food"] = relationship(back_populates="modifier_options")
    option: Mapped["ModifierOption"] = relationship()

class ModifierCategory(BaseMenuModel): # соусы
    __tablename__ = "modifier_category"
    name: Mapped[BaseModelFieldTypes.str_255]


class ModifierOption(BaseMenuModel):
    __tablename__ = "modifier_option"
    name: Mapped[BaseModelFieldTypes.str_255]
    food_modifier_option_id: Mapped[int] = mapped_column(ForeignKey("modifier_category.id"))
    price: Mapped[float]
