from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class UserCreate(BaseModel):
    """Создание пользователя."""
    username: str
    password: str

    model_config = ConfigDict(extra='forbid')


class UserDB(BaseModel):
    id: int
    username: str
