from typing import Any

from pydantic import BaseModel


# ========== Food | FoodSize | FoodType ===============

# ================== Food Type ========================

class WriteFoodTypeSchema(BaseModel):
    name: str

class ReadFoodTypeSchema(BaseModel):
    id: int
    name: str

# =================== FoodSize =========================

class WriteSingleFoodSizeSchema(BaseModel):
    name: str
    is_new: bool | None = False
    price: float

class ReadSingleFoodSizeSchema(WriteSingleFoodSizeSchema):
    id: int

# ==================== Food =============================

class WriteSingleFoodSchema(BaseModel):
    name: str
    description: str
    food_sizes: list[WriteSingleFoodSizeSchema]
    possible_food_modifiers: list[int] = []
    type_id: int


class ReadSingleFoodSchema(BaseModel):
    name: str
    id: int
    description: str
    food_type_id: int
    food_type_name: str
    food_sizes: list[ReadSingleFoodSizeSchema]
    food_modifiers: list["ReadModifierCategoryOptionSchema"]



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


# =============== Menu ===========================

class WriteSingleMenuSchema(BaseModel):
    food_id: int
    priority_level: int

class ReadSingleMenuSchema(BaseModel):
    id: int
    food_id: int
    priority_level: int


class ReadAllMenu(BaseModel):
    food_type_id: int
    food_type_name: str
    foods: list[ReadSingleFoodSchema]



