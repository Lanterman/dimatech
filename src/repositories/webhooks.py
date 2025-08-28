from sqlalchemy import select

from db.db import async_session_maker
from models.users import Accounts, Payments


async def get_user_account(account_id: int) -> Accounts | None:
    """
    Получить аккаунт пользователя, если он есть.
    Иначе вернуть None"""

    async with async_session_maker() as session:
        stmt = select(Accounts).where(Accounts.id == account_id)
        query = await session.execute(stmt)
        return query.scalar_one_or_none()


async def get_payment(transaction_id: int) -> Payments | None:
    """
    Получить аккаунт пользователя, если он есть.
    Иначе вернуть None"""

    async with async_session_maker() as session:
        stmt = select(Payments).where(Payments.transaction_id == transaction_id)
        query = await session.execute(stmt)
        return query.scalar_one_or_none()


async def create_user_account(user_id: int) -> Accounts | None:
    """Создать счет пользователя"""

    async with async_session_maker() as session:
        stmt = Accounts(user_id=user_id)
        session.add(stmt)
        await session.commit()
        return stmt


async def create_payment(account_id: int, transaction_id: int, amount: int) -> None:
    """Создать транзакцию"""

    async with async_session_maker() as session:
        stmt = Payments(amount=amount,
                        transaction_id=transaction_id,
                        account_id=account_id)
        session.add(stmt)
        await session.commit()


async def update_amount_of_user_account(user_account: Accounts) -> Accounts:
    """Обновить баланс пользовательского счета"""

    async with async_session_maker() as session:
        session.add(user_account)
        await session.commit()
