from pydantic import BaseModel, Field
from typing import Literal


class LoadImage(BaseModel):
    image: str = Field(min_length=1)
    mode: Literal['pixels', 'lines']
