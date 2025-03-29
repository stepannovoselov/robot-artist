from pydantic import BaseModel
from typing import Literal


class RobotCommand(BaseModel):
    command: Literal['clear_board', 'stop', 'start']
