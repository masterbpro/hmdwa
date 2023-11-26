from typing import Any

from pydantic import BaseModel, Field
from datetime import datetime


class Alarm(BaseModel):
    id: Any = Field(alias="_id")
    alarm_at: datetime
    reported_user: int
