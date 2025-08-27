import string
import logging
import hashlib

from random import choice
from fastapi import HTTPException, status

from models.users import Users
from repositories import users as users_repository


# Create user password
def create_random_salt(length=12) -> str:
    """Create random salt for password hashing"""

    query = "".join(choice(string.ascii_letters) for _ in range(length))
    return query


def password_hashing(password: str, salt: str = None) -> hex:
    """Password hashing with salt"""

    if salt is None:
        salt = create_random_salt()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    """Check if password matches hashed password from database"""

    salt, hashed = hashed_password.split("$")
    return password_hashing(password, salt) == hashed


# User CRUD
async def get_user_info(user_id: int) -> Users | None:
    """Get user or none"""

    user = await users_repository.get_user_info(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such user!",
        )
    
    user.full_name = f"{user.first_name} {user.last_name}"
    return user


# async def create_user(form_data: schemas.CreateUser, back_task: BackgroundTasks) -> dict:
#     """Create user"""

#     salt = create_random_salt()
#     hashed_password = password_hashing(form_data.password, salt)
#     form_data.password = f"{salt}${hashed_password}"
#     query = await Users.objects.create(**form_data.dict())

#     token = await create_user_token(user_id=query.id)
#     token_info = {"token": token.token, "expires": token.expires}

#     return {**form_data.dict(), "token": token_info}


# async def update_user_info(form_data: schemas.UpdateUserInfo, user: Users) -> Users:
#     """Update user information"""

#     updated_user = await user.update(**form_data.dict(), update_date=datetime.datetime.now())
#     return updated_user


# async def delete_user(back_task: BackgroundTasks, user: Users) -> int:
#     """Delete user"""

#     query = await user.delete()
#     return query