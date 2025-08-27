import uuid

from pydantic import BaseModel, EmailStr


class ProfileUserSchema(BaseModel):
    """Base User - schema"""

    id: int
    full_name: str
    email: EmailStr


class UserAccountSchema(BaseModel):
    """User account - schema"""

    id: int
    balance: int
    is_activated: bool


class UserPaymentSchema(BaseModel):
    """User payment - schema"""

    id: int
    amount: int
    transaction_id: uuid.UUID
    account_id: int
