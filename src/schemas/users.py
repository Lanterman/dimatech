import re
import string
import datetime

from typing import Optional
from fastapi import HTTPException, status, UploadFile
from pydantic import BaseModel, EmailStr, Field, field_validator



class ProfileUserSchema(BaseModel):
    """Base User - schema"""

    id: int
    first_name: str
    last_name: str
    email: EmailStr
