import uuid

from pydantic import BaseModel


class ReceivePayment(BaseModel):
    """Receive payment - schema"""

    transaction_id: uuid.UUID
    user_id: int
    account_id: int
    amount: int
    signature: str
