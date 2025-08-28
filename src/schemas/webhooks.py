import uuid

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class ReceivePayment(BaseModel):
    """Receive payment - schema"""

    transaction_id: uuid.UUID
    user_id: int
    account_id: int
    amount: int
    signature: str

    @field_validator("user_id")
    def check_user_id(cls, value):
        
        if value < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Field user_id(0) is not present in table 'users'")

        return value
    
    @field_validator("account_id")
    def check_account_id(cls, value):
        
        if value < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Field account_id(0) is not present in table 'users'")

        return value
