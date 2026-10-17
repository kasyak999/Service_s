from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import user_crud
from app.schemas.user import UserDB, UserCreate
# from app.services.user import access_token


router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.post(
    "/register",
    summary='Регистрация нового пользователя.',
    response_model=UserDB,
    response_model_exclude_none=True,
)
async def register(
    obj_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    **username** - имя пользователя\n
    **password** - пароль
    """
    result = await user_crud.create(obj_in, session)
    return result
