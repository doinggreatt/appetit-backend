from pydantic import BaseModel


class WriteFoodSchema(BaseModel):
    food_name: str
    modifiers: list[int] = []
    is_new: bool = False

