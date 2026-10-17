from typing import Generic, Type, TypeVar, Any, Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import Base
from app.services.user import hash_password


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс для CRUD операций с моделями."""

    def __init__(self, model: Type[ModelType]) -> None:
        """Инициализация CRUD класса с указанием модели."""
        self.model = model

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
    ):
        """Создать новый объект."""
        obj_in_data = obj_in.model_dump()
        password = obj_in_data.pop("password", None)
        if password:
            obj_in_data["hashed_password"] = hash_password(password)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        id: Any,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получить объект по id."""
        result = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        # await session.flush()
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновить существующий объект."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
