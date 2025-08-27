from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

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


@router.post("/auth", 
             response_model=users_schema.BaseToken, 
             status_code=status.HTTP_202_ACCEPTED,
             responses={400: {"description": "Incorrect email or password!"}})
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """User authenticated - endpoint"""

    token = await users_service.auth(form_data)
    return token
