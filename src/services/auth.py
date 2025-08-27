import os
import jwt
import logging
import secrets

from datetime import datetime

from fastapi import HTTPException, status

from models import users as users_model
from repositories import auth as auth_repository, users as users_repository
from services import users as users_service


async def auth(form_data: dict) -> users_model.Users | None:
    """Authentication"""

    user = await users_repository.get_user_by_email(form_data.username)
    error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")

    if user is None:
        raise error

    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user!")

    if not users_service.validate_password(form_data.password, user.hashed_password):
        raise error

    token = await create_user_token(user_id=user.id)
    return token



# Auth - dependence
async def base_auth(token: str) -> users_model.Tokens | None:
    """Base auth"""

    token_db, user_db = await auth_repository.get_user_token(token)

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


async def get_user_by_token(token: str) -> users_model.Tokens | None:
    """Get user by token"""

    user: users_model.Users = await base_auth(token)
    return user


async def get_admin_by_token(token: str) -> users_model.Tokens | None:
    """Get admin by token"""

    admin: users_model.Users = await base_auth(token)

    if not admin.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission!")
    
    return admin



# JWTToken
async def create_user_token(user_id: int) -> users_model.Tokens:
    """Create user token"""

    await delete_user_token(user_id)

    _secret_key = await create_user_secret_key(user_id=user_id)

    logging.info(f"Новый секретный ключ: {_secret_key}")

    _token = jwt.encode(payload={"user_id": user_id}, key=_secret_key, algorithm=os.environ["ALGORITHM"])

    logging.info(f"Новый токен: {_token}")

    token = await auth_repository.create_user_token(_token, user_id)
    return token


async def delete_user_token(user_id: int) -> None:
    """Delete user token"""

    await auth_repository.delete_user_token(user_id)


async def create_user_secret_key(user_id: int) -> str:
    """Create random user secret"""

    random_string = secrets.token_hex()

    await delete_user_secret_key(user_id)
    secret_key = await auth_repository.create_user_secret_key(random_string, user_id)
    return secret_key.secret_key


async def delete_user_secret_key(user_id: int) -> None:
    """Delete user token"""

    await auth_repository.delete_user_secret_key(user_id)
