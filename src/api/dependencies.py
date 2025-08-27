from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from services import users as users_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> users_service.Users:
    """Authenticated user with jwt"""

    user = await users_service.get_user_by_token(token)
    return user
