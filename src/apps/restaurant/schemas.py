from pydantic import BaseModel

class WriteSingleRestaurantSchema(BaseModel):
    name: str

class ReadSingleRestaurantSchema(WriteSingleRestaurantSchema):
    id: int
