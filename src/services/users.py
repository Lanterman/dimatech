import os
import jwt
import string
import secrets
import hashlib
import datetime

from random import choice
from fastapi import BackgroundTasks

from models.users import Users, Tokens, SecretKeys
from repositories import users as users_repository


# Create user password
# def create_random_salt(length=12) -> str:
#     """Create random salt for password hashing"""

#     query = "".join(choice(string.ascii_letters) for _ in range(length))
#     return query


# def password_hashing(password: str, salt: str = None) -> hex:
#     """Password hashing with salt"""

#     if salt is None:
#         salt = create_random_salt()
#     enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
#     return enc.hex()


# def validate_password(password: str, hashed_password: str) -> bool:
#     """Check if password matches hashed password from database"""

#     salt, hashed = hashed_password.split("$")
#     return password_hashing(password, salt) == hashed


# JWT Token
# async def create_random_user_secret_key(user_id: int) -> hex:
#     """Create random user secret"""

#     query = secrets.token_hex()

#     await delete_user_secret_key(user_id)
#     await SecretKeys.objects.create(secret_key=query, user=user_id)

#     return query


async def get_user_token(token: str) -> Tokens | None:
    """Get user token"""

    query = await Tokens.objects.select_related("user").get_or_none(
        token=token, expires__gt=datetime.datetime.now()
    )
    return query


# async def delete_user_secret_key(user_id: int) -> None:
#     """Delete user token"""

#     await SecretKeys.objects.delete(user=user_id)


# async def delete_user_token(user_id: int) -> None:
#     """Delete user token"""

#     await Tokens.objects.delete(user=user_id)


# async def create_user_token(user_id: int) -> Tokens:
#     """Create user token"""

#     await delete_user_token(user_id)

#     _secret_key = await create_random_user_secret_key(user_id=user_id)
#     _token = jwt.encode(payload={"user_id": user_id}, key=_secret_key, algorithm=os.environ["ALGORITHM"])
#     query = await Tokens.objects.create(token=_token, user=user_id)
#     return query


# User CRUD
async def get_user_info(user_id: int) -> Users | None:
    """Get user or none"""

    user = await users_repository.get_user_info(user_id)
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


async def delete_user(back_task: BackgroundTasks, user: Users) -> int:
    """Delete user"""

    query = await user.delete()
    return query