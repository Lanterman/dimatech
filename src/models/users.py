from datetime import datetime, timedelta
from typing import List, Annotated

from pydantic import EmailStr
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


intpk = Annotated[int, mapped_column(primary_key=True, index=True)]


class Users(Base):
    """User entities"""

    __tablename__ = "users"

    id: Mapped[intpk]
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[EmailStr] = mapped_column(String(50), unique=True, index=True)
    is_activated: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column(String(100))
    accounts: Mapped[List["Accounts"]] = relationship("Accounts", back_populates="user")
    token: Mapped[List["Tokens"]] = relationship("Tokens", back_populates="user")
    secret_key: Mapped[List["SecretKeys"]] = relationship("SecretKeys", back_populates="user")


class Accounts(Base):
    """Account entities"""

    __tablename__ = "accounts"

    id: Mapped[intpk]
    balance: Mapped[int] = mapped_column(Integer)
    is_activated: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="accounts")
    payments: Mapped[List["Payments"]] = relationship("Payments", back_populates="account")


class Payments(Base):
    """Payment entities"""

    __tablename__ = "payments"

    id: Mapped[intpk]
    amount: Mapped[int] = mapped_column(Integer)
    is_activated: Mapped[bool] = mapped_column(default=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    account: Mapped["Accounts"] = relationship(back_populates="payments")


class SecretKeys(Base):
    """Secret Key entities"""

    __tablename__ = "secret_keys"

    id: Mapped[intpk]
    secret_key: Mapped[str] = mapped_column(String(150), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="secret_key")


class Tokens(Base):
    """Token entities"""

    __tablename__ = "tokens"

    id: Mapped[intpk]
    token: Mapped[str] = mapped_column(String(300), unique=True, index=True)
    expires: Mapped[datetime] = mapped_column(DateTime, default=datetime.now() + timedelta(weeks=1))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="token")
