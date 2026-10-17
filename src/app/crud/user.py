from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import User
from app.crud.base_crud import CRUDBase


class UserCrud(CRUDBase):
    """CRUD операции для модели User."""


user_crud = UserCrud(User)
