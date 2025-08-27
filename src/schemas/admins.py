import uuid

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator

from schemas import users as users_schema


class ValidationUserClass:
    """Класс, который содержит проверки всех полей, но не в этом проекте)"""

    @field_validator("first_name")
    def check_first_last(cls, value):
        
        if len(value) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Min length first name is 5 character!")

        return value
    
    @field_validator("last_name")
    def check_last_name(cls, value):
        
        if len(value) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Min length last name is 5 character!")

        return value
    
    @field_validator("is_activated")
    def check_is_activated(cls, value):

        if type(value) != bool:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data type. 'bool' required")
        
        return value
    
    @field_validator("is_admin")
    def check_is_admin(cls, value):

        if type(value) != bool:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data type. 'bool' required")
        
        return value

    
class BaseUserSchema(BaseModel):
    """Base user - schema"""

    first_name: str
    last_name: str
    email: EmailStr
    is_activated: bool
    is_admin: bool


class ProfileAdminSchema(BaseModel):
    """Admin Profile - schema"""

    id: int
    full_name: str
    email: EmailStr
    is_admin: bool


class UserSchema(users_schema.ProfileUserSchema):
    """User and his accounts - schema"""

    is_activated: bool
    is_admin: bool
    accounts: list[users_schema.UserAccountSchema]


class CreateUserSchema(ValidationUserClass, BaseUserSchema):
    """Create user - schema"""

    password1: str
    password2: str

    @property


    @field_validator("email")
    def check_email(cls, value):

        string_before_dog = value.split("@")[0]
        
        if len(string_before_dog) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Min length email is 5 character!")

        return value
    
    @field_validator("password1")
    def check_password1(cls, value):
        """Check password1"""

        if len(value) < 10:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too simple!")

        return value
    
    @field_validator("password2")
    def check_password2(cls, value, values):
        """Check password2"""

        if value != values.data["password1"]:
            raise HTTPException(detail="Passwords do not match!", status_code=status.HTTP_400_BAD_REQUEST)

        return value


class UpdateUserSchema(ValidationUserClass, BaseModel):
    """Update user - schema"""

    first_name: str
    last_name: str
    is_activated: bool
    is_admin: bool