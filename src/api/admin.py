from fastapi import Depends, APIRouter, status

from .dependencies import get_current_admin
from services import admins as admins_service
from schemas import admins as admins_schema
from models.users import Users


router = APIRouter(prefix="/admins", tags=["admins"])


@router.get("/profile", 
            response_model=admins_schema.ProfileAdminSchema,
            status_code=status.HTTP_200_OK,
            responses={404: {"description": "No such admin!"},
                       403: {"description": "You don't have permission!"},
                       401: {"description": "Invalid authentication credentials"}})
async def get_profile(current_user: Users = Depends(get_current_admin)):
    """Get admin info - endpoint"""

    admin_info = await admins_service.get_admin_info(current_user.id)
    return admin_info


@router.get("/users", 
            response_model=list[admins_schema.UserSchema], 
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "You don't have permission!"},
                       401: {"description": "Invalid authentication credentials"}})
async def get_users(current_user: Users = Depends(get_current_admin)):
    """Get users and their accounts - endpoint"""

    users = await admins_service.get_users()
    return users


@router.get("/users/{user_id}", 
            response_model=admins_schema.UserSchema, 
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "You don't have permission!"},
                       401: {"description": "Invalid authentication credentials"}})
async def get_user(user_id: int, current_user: Users = Depends(get_current_admin)):
    """Get user and his accounts - endpoint"""

    user = await admins_service.get_user(user_id)
    return user


@router.post("/users", 
            response_model=admins_schema.BaseUserSchema, 
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "You don't have permission!"},
                       401: {"description": "Invalid authentication credentials"},
                       400: {"description": "A user with this email address already exists!"}})
async def create_user(
    form_data: admins_schema.CreateUserSchema, 
    current_user: Users = Depends(get_current_admin)
):
    """Create user - endpoint"""

    user = await admins_service.create_user(form_data)
    return user


@router.put("/users/{user_id}", 
            response_model=admins_schema.UpdateUserSchema, 
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "You don't have permission!"},
                       401: {"description": "Invalid authentication credentials"},
                       400: {"description": "A user with this email address already exists!"}})
async def update_user(
    user_id: int,
    form_data: admins_schema.UpdateUserSchema, 
    current_user: Users = Depends(get_current_admin)
):
    """Update user - endpoint"""

    user = await admins_service.update_user(user_id, form_data)
    return user


@router.delete("/users/{user_id}",  
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "You don't have permission!"},
                       401: {"description": "Invalid authentication credentials"}})
async def delete_user(
    user_id: int,
    current_user: Users = Depends(get_current_admin)
):
    """Delete user - endpoint"""

    await admins_service.delete_user(user_id)
    return {"detail": f"User {user_id} is deleted!"}
