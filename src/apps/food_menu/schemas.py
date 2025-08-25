from typing import Any

from pydantic import BaseModel


# ========== Food | FoodSize | FoodType ===============

# ================== Food Type ========================

class WriteFoodType(BaseModel):
    name: str

class ReadFoodType(BaseModel):
    id: int
    name: str

# =================== FoodSize =========================

class WriteFoodSizeSchema(BaseModel):
    name: str
    is_new: bool | None = False
    price: float

class ReadFoodSizeSchema(WriteFoodSizeSchema):
    id: int

# ==================== Food =============================

class WriteFoodSchema(BaseModel):
    name: str
    food_sizes: list[WriteFoodSizeSchema]
    possible_food_modifiers: list[int] = []
    type_id: int


# =========== Modifier | Modifier Option =========

class WriteModifierCategorySchema(BaseModel):
    name: str

class ReadModifierCategorySchema(WriteModifierCategorySchema):
    id: int

class WriteModifierOptionSchema(BaseModel):
    modifier_category_id: int
    name: str
    price: float

class ReadModifierOptionSchema(WriteModifierOptionSchema):
    id: int

class ReadSingleModifierOptionSchema(BaseModel):
    id: int
    name: str
    price: float

class ReadModifierCategoryOptionSchema(BaseModel):
    modifier_cat_id: int
    modifier_cat_name: str
    modifier_options: list[ReadSingleModifierOptionSchema] | list[None] = []