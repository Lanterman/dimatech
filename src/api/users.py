from fastapi import Depends, APIRouter

from .dependencies import get_current_user
from services import users as users_service
from schemas.users import ProfileUserSchema
from models.users import Users


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=ProfileUserSchema)
async def profile(current_user: Users = Depends(get_current_user)):
    """Get user info - endpoint"""

    user_info = await users_service.get_user_info(current_user.id)
    return user_info
