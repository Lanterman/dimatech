from sqlalchemy import select
from models.users import Users, Tokens, SecretKeys
from db.db import async_session_maker


# Token
async def get_user_token(token: str) -> tuple[Tokens, Users] | None:
    """Get user token"""

    async with async_session_maker() as session:
        stmt = select(Tokens, Users).join(Users).where(Tokens.token == token)
        query = await session.execute(stmt)
        result = query.first()
        return (None, None) if result is None else result


async def create_user_token(token: str, user_id: int) -> Tokens:
    """Создать токен для пользователя"""

    async with async_session_maker() as session:
        stmt = Tokens(token=token, user_id=user_id)
        session.add(stmt)
        await session.commit()
        return stmt


async def delete_user_token(user_id: int) -> None:
    """Удалить токен пользователя, если он есть"""

    async with async_session_maker() as session:
        stmt = select(Tokens).where(Tokens.user_id == user_id)
        query = await session.execute(stmt)
        token = query.scalar_one_or_none()

        if token is not None:
            await session.delete(token)
            await session.commit()


async def create_user_secret_key(secret_key: str, user_id: int) -> SecretKeys:
    """Создать секретный ключ пользователя"""

    async with async_session_maker() as session:
        stmt = SecretKeys(secret_key=secret_key, user_id=user_id)
        session.add(stmt)
        await session.commit()
        return stmt


async def delete_user_secret_key(user_id: int) -> None:
    """Удалить секретный ключ пользователя, если он есть"""

    async with async_session_maker() as session:
        stmt = select(SecretKeys).where(SecretKeys.user_id == user_id)
        query = await session.execute(stmt)
        secret_key = query.scalar_one_or_none()

        if secret_key is not None:
            await session.delete(secret_key)
            await session.commit()
