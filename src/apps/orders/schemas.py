from pydantic import BaseModel

class WriteSingleOrderSchema(BaseModel):
    food_ids: list[int]
    food_size_ids: list[int]
    modifier_option_ids: list[int]
    order_address: str | None
    is_payed: bool | None = False
    address: str | None = None
