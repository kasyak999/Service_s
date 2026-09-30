from app.core.db import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SQLEnum
import enum


class RequestStatus(str, enum.Enum):
    DRAFT = "Создано АСЦ"
    IN_REVIEW = "На рассмотрении"
    APPROVED = "Собирается"
    SHIPPED = "Отгружена / В пути"
    COMPLETED = "Получено АСЦ"


class PartsRequest(Base):
    """Модель запросов на запчасти"""
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(RequestStatus, native_enum=False),
        default=RequestStatus.DRAFT,
        comment='Статус запроса')
    is_urgent: Mapped[bool] = mapped_column(
        default=False,
        comment='Срочный/гарантийный ремонт')
    work_order_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment='№ акта приема/заказа АСЦ')
    device_model: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Модель устройства')
    serial_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='Серийный номер техники')
    comment_asc: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment='Примечание')
    asc_id: Mapped[int] = mapped_column(
        ForeignKey('servicecenter.id', ondelete="CASCADE"),
        nullable=False,
        comment='АСЦ')
    asc: Mapped["ServiceCenter"] = relationship(  # noqa: F821
        "ServiceCenter", back_populates="parts_requests")

    def __repr__(self) -> str:
        return f'{self.device_model}'
