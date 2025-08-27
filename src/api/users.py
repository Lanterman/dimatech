from fastapi import Depends, APIRouter, status

from .dependencies import get_current_user
from services import users as users_service
from schemas import users as users_schema
from models.users import Users


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", 
            response_model=users_schema.ProfileUserSchema, 
            status_code=status.HTTP_200_OK,
            responses={404: {"description": "No such user!"},
                       401: {"description": "Invalid authentication credentials"}})
async def profile(current_user: Users = Depends(get_current_user)):
    """Get user info - endpoint"""

    user_info = await users_service.get_user_info(current_user.id)
    return user_info


@router.get("/accounts", 
            response_model=list[users_schema.UserAccountSchema], 
            status_code=status.HTTP_200_OK,
            responses={401: {"description": "Invalid authentication credentials"}})
async def accounts(current_user: Users = Depends(get_current_user)):
    """Get user accounts - endpoint"""

    accounts = await users_service.get_accounts(current_user.id)
    return accounts


@router.get("/payments", 
            response_model=list[users_schema.UserPaymentSchema], 
            status_code=status.HTTP_200_OK,
            responses={401: {"description": "Invalid authentication credentials"}})
async def payments(current_user: Users = Depends(get_current_user)):
    """Get user payments - endpoint"""

    payments = await users_service.get_payments(current_user.id)
    return payments
