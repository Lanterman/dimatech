import datetime

from typing import Optional
from pydantic import BaseModel, Field


class BaseToken(BaseModel):
    """Base token - schema"""

    token: str = Field(..., alias="access_token")
    expires: datetime.datetime
    type: Optional[str] = "Bearer"

    class Config:
        validate_by_name = True
