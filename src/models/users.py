import ormar

from datetime import datetime
from pydantic import EmailStr

from config.utils import base_ormar_config

class Users(ormar.Model):
    """User entities"""

    ormar_config = base_ormar_config.copy(tablename="users")
    
    id: int = ormar.Integer(primary_key=True, index=True)
    first_name: str = ormar.String(max_length=50)
    last_name: str = ormar.String(max_length=50)
    email: EmailStr = ormar.String(max_length=50, unique=True, index=True)
    is_activated: bool = ormar.Boolean(default=True)
    is_admin: bool = ormar.Boolean(default=False)
    hashed_password: str = ormar.String(max_length=100)


class Accounts(ormar.Model):
    """Account entities"""

    ormar_config = base_ormar_config.copy(tablename="accounts")
    
    id: int = ormar.Integer(primary_key=True, index=True)
    balance: int = ormar.Integer()
    is_activated: bool = ormar.Boolean(default=True)
    user_id: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="accounts")


class Payments(ormar.Model):
    """Payment entities"""

    ormar_config = base_ormar_config.copy(tablename="payments")

    id: int = ormar.Integer(primary_key=True, index=True)
    amount: int = ormar.Integer()
    account_id: int = ormar.ForeignKey(to=Accounts, ondelete="CASCADE", related_name="accounts")


class SecretKeys(ormar.Model):
    """Secret Key entities"""

    ormar_config = base_ormar_config.copy(tablename="secret_keys")

    id: int = ormar.Integer(primary_key=True, index=True)
    secret_key: str = ormar.String(max_length=300, unique=True)
    user: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="secret_key_set")


class Tokens(ormar.Model):
    """Token entities"""

    ormar_config = base_ormar_config.copy(tablename="tokens")

    id: int = ormar.Integer(primary_key=True, index=True)
    token: str = ormar.String(max_length=300, index=True, unique=True)
    expires: datetime.datetime = ormar.DateTime(default=datetime.datetime.now() + datetime.timedelta(weeks=1))
    user: int = ormar.ForeignKey(to=Users, ondelete="CASCADE", related_name="token_set")
