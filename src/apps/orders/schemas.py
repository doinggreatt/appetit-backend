from pydantic import BaseModel


class WriteSingleOrderSchema(BaseModel):
    food_ids: list[int]
    food_size_ids: list[int]
    modifier_option_ids: list[int]
    is_payed: bool | None = False
    restaurant_id: int = None

class ReadSingleOrderSchema(BaseModel):
    id: int

