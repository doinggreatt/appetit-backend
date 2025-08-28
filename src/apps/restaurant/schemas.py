from pydantic import BaseModel

class WriteSingleRestaurantSchema(BaseModel):
    name: str
    lat: float
    lon: float

class ReadSingleRestaurantSchema(WriteSingleRestaurantSchema):
    id: int
