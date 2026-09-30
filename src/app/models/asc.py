from app.core.db import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey


class ServiceCenter(Base):
    """Модель сервисных центров"""
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Название АСЦ',
    )
    contact_person: Mapped[str | None] = mapped_column(
        String(255),
        nullable=False,
        comment='Контактное лицо',
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment='Номер телефона'
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=False,
        comment='Email для уведомлений'
    )
    address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment='Адрес доставки деталей'
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        comment='Статус активности'
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        comment="Пользователь"
    )
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="asc")
    parts_requests: Mapped[list["PartsRequest"]] = relationship(  # noqa: F821
            "PartsRequest",
            back_populates="asc",
            cascade="all, delete-orphan",
            order_by="PartsRequest.id"
        )

    def __repr__(self) -> str:
        return f'{self.name}'
