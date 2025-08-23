from typing import Optional

from pydantic import BaseModel, Field, model_validator, EmailStr


class UserWriteSchema(BaseModel):
    first_name: str 
    last_name: str
    email: EmailStr
    password: str
    password_2: str

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "UserWriteSchema":
        if self.password != self.password_2:
            raise ValueError("password should match")
        return self


class UserReadSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str 
    last_name: str 
    
    
class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    password_2: Optional[str] = None

class AccessTokenLoginSchema(BaseModel):
    email: EmailStr
    password: str