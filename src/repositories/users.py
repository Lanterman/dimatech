from sqlalchemy import select
from pydantic import EmailStr
from models.users import Users, Accounts, Payments
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


async def get_accounts(user_id: int) -> list[Accounts]:
    """Получить счетов пользователя"""

    async with async_session_maker() as session:
        stmt = select(Accounts).where(Accounts.user_id == user_id)
        query = await session.execute(stmt)
        return query.scalars().all()


async def get_payments(user_id: int) -> list[Payments]:
    """Получить транзакции пользователя"""

    async with async_session_maker() as session:
        stmt = select(Payments, Accounts).join(Accounts).where(Accounts.user_id == user_id)
        query = await session.execute(stmt)
        return query.scalars().all()
