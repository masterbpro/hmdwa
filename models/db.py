from typing import Any

from pydantic import BaseModel, Field
from datetime import datetime


class Alarm(BaseModel):
    id: Any = Field(alias="_id")
    alarm_at: datetime
    reported_user: int


class User(BaseModel):
    id: Any = Field(alias="_id")
    username: str = None
    first_name: str
    last_name: str
    language_code: str
    create_date: datetime
