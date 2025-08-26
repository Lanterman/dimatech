from models.users import Users, Tokens, SecretKeys


async def get_user_info(self, user_id: int):
    """
    Получить пользователя, если он есть
    Иначе вернуть None
    """
    
    user = await Users.objects.get_or_none(id=user_id)
    return user
