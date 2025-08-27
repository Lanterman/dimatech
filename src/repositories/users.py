from sqlalchemy import select
from pydantic import EmailStr
from models.users import Users
from db.db import async_session_maker


async def get_user_by_email(user_email: EmailStr) -> Users | None:
    """
    Получить пользователя по 'email', если он есть
    Иначе вернуть None
    """

    async with async_session_maker() as session:
        stmt = select(Users).where(Users.email == user_email)
        query = await session.execute(stmt)
        return query.scalar_one_or_none()


async def get_user_info(user_id: int) -> Users | None:
    """
    Получить пользователя по 'ID', если он есть
    Иначе вернуть None
    """

    async with async_session_maker() as session:
        stmt = select(Users).where(Users.id == user_id)
        query = await session.execute(stmt)
        return query.scalar_one_or_none()
