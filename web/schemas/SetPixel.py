from pydantic import BaseModel, field_validator
from pydantic import ValidationError
from typing import Literal
from config import PIXELS_X, PIXELS_Y


class SetPixel(BaseModel):
    x: int
    y: int
    color: Literal['black', 'white', 'red']

    @field_validator('x', mode='after')
    @classmethod
    def check_x(cls, x):
        if x > PIXELS_X or 0 > x:
            raise ValidationError
        return x

    @field_validator('y', mode='after')
    @classmethod
    def check_y(cls, y):
        if y > PIXELS_Y or 0 > y:
            raise ValidationError
        return y

