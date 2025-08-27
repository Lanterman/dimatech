import logging.handlers
import os
import jwt
import string
import logging
import secrets
import hashlib

from datetime import datetime
from random import choice
from fastapi import HTTPException, status

from models.users import Users, Tokens, SecretKeys
from repositories import users as users_repository


async def get_user_by_token(token: str) -> Tokens | None:
    """Get user token"""

    token_db, user_db = await users_repository.get_user_token(token)

    if token_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticated": "Bearer"}
        )

    if token_db.expires <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired!",
            headers={"WWW-Authenticated": "Bearer"}
        )

    if not user_db.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user!")
    
    return user_db


async def auth(form_data: dict) -> Users | None:
    """Authentication"""

    user = await users_repository.get_user_by_email(form_data.username)
    error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    if user is None:
        raise error

    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user!")

    # if not validate_password(form_data.password, user.hashed_password):
    #     raise error

    token = await create_user_token(user_id=user.id)
    return token



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



# Token
async def create_user_token(user_id: int) -> Tokens:
    """Create user token"""

    await delete_user_token(user_id)

    _secret_key = await create_random_user_secret_key(user_id=user_id)

    logging.info(f"Новый секретный ключ: {_secret_key}")

    _token = jwt.encode(payload={"user_id": user_id}, key=_secret_key, algorithm=os.environ["ALGORITHM"])

    logging.info(f"Новый токен: {_token}")

    token = await users_repository.create_user_token(_token, user_id)
    return token


async def delete_user_token(user_id: int) -> None:
    """Delete user token"""

    await users_repository.delete_user_token(user_id)


async def create_random_user_secret_key(user_id: int) -> str:
    """Create random user secret"""

    random_string = secrets.token_hex()

    await delete_user_secret_key(user_id)
    secret_key = await users_repository.create_user_secret_key(random_string, user_id)
    return secret_key.secret_key


async def delete_user_secret_key(user_id: int) -> None:
    """Delete user token"""

    await users_repository.delete_user_secret_key(user_id)



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