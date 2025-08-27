from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from db.db import async_session_maker

from repositories import users as users_repository
from schemas import admins as admins_schema
from models.users import Users


async def get_admin_info(user_id: int) -> Users | None:
    """
    Получить админа по 'ID', если он есть
    Иначе вернуть None
    """

    admin = await users_repository.get_user_info(user_id)
    return admin


async def get_users() -> list[Users]:
    """Получить пользователей и их аккаунты"""

    async with async_session_maker() as session:
        stmt = select(Users).options(selectinload(Users.accounts))
        query = await session.execute(stmt)
        return query.scalars().all()


async def get_user(user_id: int) -> Users | None:
    """
    Получить пользователя и его аккаунты, если такой пользователь есть
    Иначе получить None
    """

    async with async_session_maker() as session:
        stmt = select(Users).options(selectinload(Users.accounts)).where(Users.id == user_id)
        query = await session.execute(stmt)
        return query.scalar_one_or_none()


async def create_user(hashed_password: str, form_data: admins_schema.BaseUserSchema) -> Users:
    """Создать нового пользователя"""

    async with async_session_maker() as session:
        stmt = Users(hashed_password=hashed_password, **form_data.model_dump())
        session.add(stmt)
        await session.commit()
        return stmt


async def update_user(user_id: int, form_data: admins_schema.UpdateUserSchema) -> Users | None:
    """Обновить пользователя"""

    async with async_session_maker() as session:
        stmt = select(Users).where(Users.id == user_id)
        query = await session.execute(stmt)
        user = query.scalar_one_or_none()

        if user is not None:
            user.first_name = form_data.first_name
            user.last_name = form_data.last_name
            user.is_activated = form_data.is_activated
            user.is_admin = form_data.is_admin
            session.add(user)
            await session.commit()
            return user


async def delete_user(user_id: int) -> int | None:
    """Удалить пользователя"""

    async with async_session_maker() as session:
        stmt = delete(Users).where(Users.id == user_id)
        await session.execute(stmt)
        await session.commit()

        
