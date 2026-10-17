from app.core.db import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """Модель пользователя."""
    username: Mapped[str] = mapped_column(
        unique=True,
        comment='Логин',
    )
    is_superuser: Mapped[bool] = mapped_column(
        comment='Роль суперпользователя',
    )
    hashed_password: Mapped[str] = mapped_column(
        comment='Хеш пароля',
    )
    asc: Mapped[list["ServiceCenter"]] = relationship(  # noqa: F821
        "ServiceCenter",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="ServiceCenter.id"
    )

    def __repr__(self) -> str:
        return f'{self.username}'
