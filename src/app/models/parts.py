from app.core.db import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Text, Integer, ForeignKey, Enum as SQLEnum, JSON)
import enum


class RequestStatus(str, enum.Enum):
    CREATED = "Создано"
    IN_REVIEW = "На рассмотрении"
    COLLECTING = "Собирается"
    SHIPPED = "Отправлено"


class PartsRequest(Base):
    """Модель запросов на запчасти"""
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(RequestStatus, native_enum=False),
        default=RequestStatus.CREATED,
        comment='Статус запроса')
    is_urgent: Mapped[bool] = mapped_column(
        comment='Платный/гарантийный ремонт')
    work_order_number: Mapped[str] = mapped_column(
        String(100),
        comment='№ акта')
    device_model: Mapped[str] = mapped_column(
        String(255),
        comment='Модель устройства')
    serial_number: Mapped[str] = mapped_column(
        String(100),
        comment='Серийный номер техники')
    comment_asc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment='Примечание')
    files: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
        comment='Акты и фотографии'
    )
    asc_id: Mapped[int] = mapped_column(
        ForeignKey('servicecenter.id', ondelete="CASCADE"),
        nullable=False,
        comment='АСЦ')
    asc: Mapped["ServiceCenter"] = relationship(  # noqa: F821
        "ServiceCenter", back_populates="parts_requests")

    def __repr__(self) -> str:
        return f'{self.device_model}'
