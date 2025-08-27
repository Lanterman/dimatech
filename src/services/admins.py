import logging

from fastapi import HTTPException, status

from models.users import Users, Accounts, Payments
from repositories import admins as admins_repository
from repositories import users as users_repository
from schemas import admins as admins_schema
from services import users as users_service
from config import utils


async def get_admin_info(user_id: int) -> Users | None:
    """Get admin info"""

    user = await admins_repository.get_admin_info(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such admin!",
        )
    
    user.full_name = f"{user.first_name} {user.last_name}"
    return user


async def get_users() -> list[Users]:
    """Get users and their accounts"""

    users = await admins_repository.get_users()
    logging.info(f"Количество пользователей: {len(users)}")

    for user in users:
        user.full_name = utils.get_full_name(user.first_name, user.last_name)

    return users


async def get_user(user_id: int) -> Users:
    """Get user and his accounts"""

    user = await admins_repository.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such user!",
        )

    user.full_name = utils.get_full_name(user.first_name, user.last_name)
    return user


async def create_user(form_data: admins_schema.BaseUserSchema) -> Users:
    """Create user"""

    user = await users_repository.get_user_by_email(form_data.email)

    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email address already exists!")

    salt = users_service.create_random_salt()
    hashed_password = users_service.password_hashing(form_data.password1, salt)
    hashed_password = f"{salt}${hashed_password}"

    del form_data.password1
    del form_data.password2

    user = await admins_repository.create_user(hashed_password, form_data)
    logging.info(f"User {user.id} was updated!")
    return user


async def update_user(user_id: int, form_data: admins_schema.CreateUserSchema) -> Users:
    """Update user"""

    user = await admins_repository.update_user(user_id, form_data)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user!")

    logging.info(f"User {user.id} was updated!")
    
    return user


async def delete_user(user_id: int) -> None:
    """Delete user"""

    await admins_repository.delete_user(user_id)
