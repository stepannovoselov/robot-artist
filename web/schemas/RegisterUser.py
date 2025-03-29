from pydantic import BaseModel, EmailStr, Field


class RegisterUser(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    password: str = Field(min_length=1)
