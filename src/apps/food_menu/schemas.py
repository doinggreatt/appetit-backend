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
    food_name: str
    food_sizes: list[WriteFoodSizeSchema]
    is_new: bool
    possible_food_modifiers: list[int]

# =========== Modifier | Modifier Option =========

class WriteModifierCategorySchema(BaseModel):
    name: str

class WriteModifierOptionSchema(BaseModel):
    modifier_category_id: id
    name: str
    price: float
