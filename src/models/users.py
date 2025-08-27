import uuid

from datetime import datetime, timedelta
from typing import List, Annotated

from pydantic import EmailStr
from sqlalchemy import Integer, String, ForeignKey, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


intpk = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)]


class Users(Base):
    """User entities"""

    __tablename__ = "users"

    id: Mapped[intpk]
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(50), unique=True, index=True, nullable=False)
    is_activated: Mapped[bool] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    accounts: Mapped[List["Accounts"]] = relationship("Accounts", back_populates="user")
    token: Mapped[List["Tokens"]] = relationship("Tokens", back_populates="user")
    secret_key: Mapped[List["SecretKeys"]] = relationship("SecretKeys", back_populates="user")


class Accounts(Base):
    """Account entities"""

    __tablename__ = "accounts"

    id: Mapped[intpk]
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    is_activated: Mapped[bool] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="accounts")
    payments: Mapped[List["Payments"]] = relationship("Payments", back_populates="account")


class Payments(Base):
    """Payment entities"""

    __tablename__ = "payments"

    id: Mapped[intpk]
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_id: Mapped[uuid.UUID] = mapped_column(Uuid, unique=True, nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    account: Mapped["Accounts"] = relationship(back_populates="payments")


class SecretKeys(Base):
    """Secret Key entities"""

    __tablename__ = "secret_keys"

    id: Mapped[intpk]
    secret_key: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="secret_key")


class Tokens(Base):
    """Token entities"""

    __tablename__ = "tokens"

    id: Mapped[intpk]
    token: Mapped[str] = mapped_column(String(300), unique=True, index=True, nullable=False)
    expires: Mapped[datetime] = mapped_column(DateTime, default=datetime.now() + timedelta(weeks=1), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="token")
