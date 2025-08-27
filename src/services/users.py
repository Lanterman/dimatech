import string
import logging
import hashlib

from random import choice
from fastapi import HTTPException, status

from models.users import Users, Accounts, Payments
from repositories import users as users_repository
from config import utils


# Create user password
def create_random_salt(length=12) -> str:
    """Create random salt for password hashing"""

    query = "".join(choice(string.ascii_letters) for _ in range(length))
    return query


def password_hashing(password: str, salt: str = None) -> str:
    """Password hashing with salt"""

    if salt is None:
        salt = create_random_salt()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    """Check if password matches hashed password from database"""

    print(password, hashed_password)
    try:
        salt, hashed = hashed_password.split("$")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password!")
    
    print(password_hashing(password, salt) == hashed, password_hashing(password, salt), hashed)
    return password_hashing(password, salt) == hashed


async def get_user_info(user_id: int) -> Users | None:
    """Get user info"""

    user = await users_repository.get_user_info(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such user!",
        )
    
    user.full_name = utils.get_full_name(user.first_name, user.last_name)
    return user


async def get_accounts(user_id: int) -> list[Accounts]:
    """Get user accounts"""

    accounts = await users_repository.get_accounts(user_id)
    logging.info(f"Количество счетов пользователя '{user_id}': {len(accounts)}")
    return accounts


async def get_payments(user_id: int) -> list[Accounts]:
    """Get user payments"""

    payments = await users_repository.get_payments(user_id)
    logging.info(payments[0].transaction_id)
    logging.info(f"Количество транзакций пользователя '{user_id}': {len(payments)}")
    return payments
