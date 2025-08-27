import re
import string
import datetime

from typing import Optional
from fastapi import HTTPException, status, UploadFile
from pydantic import BaseModel, EmailStr, Field, field_validator


class BaseToken(BaseModel):
    """Base token - schema"""

    token: str = Field(..., alias="access_token")
    expires: datetime.datetime
    type: Optional[str] = "Bearer"

    class Config:
        validate_by_name = True


class ProfileUserSchema(BaseModel):
    """Base User - schema"""

    id: int
    full_name: str
    email: EmailStr
