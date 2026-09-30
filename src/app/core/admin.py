from datetime import timezone
from zoneinfo import ZoneInfo

from sqlalchemy import inspect
from sqladmin import ModelView
from sqladmin.filters import BooleanFilter

from app.models import User, PartsRequest, ServiceCenter
from app.models.parts import RequestStatus
from wtforms import SelectField


def to_moscow(dt):
    """Преобразовать время в московское"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(
        ZoneInfo("Europe/Moscow")).strftime("%d.%m.%Y %H:%M:%S %Z")


def get_column_comments(model):
    """Получить комментарии к столбцам модели для отображения в админке"""
    mapper = inspect(model)
    labels = {}
    for column in mapper.columns:
        if column.comment:
            labels[column.name] = column.comment
    return labels


class UserAdmin(ModelView, model=User):
    """Административный интерфейс для модели User."""
    column_list = [
        User.username,
        User.is_superuser,
    ]
    name = "пользователь"
    name_plural = "Пользователи"
    column_labels = {**get_column_comments(User)}
    column_formatters = {
        User.created_at: lambda m, _: to_moscow(m.created_at)}
    column_formatters_detail = column_formatters
    # form_excluded_columns = [
    #     'created_at', 'hashed_password', 'username']
    # can_create = False
    column_filters = [
        BooleanFilter(User.is_superuser, title="Права администратора"),
    ]
    column_sortable_list = [
        User.username,
        User.is_superuser,
    ]


class ServiceCenterAdmin(ModelView, model=ServiceCenter):
    """Административный интерфейс для модели ServiceCenter."""
    column_list = [
        ServiceCenter.name,
        ServiceCenter.contact_person,
        ServiceCenter.phone,
        ServiceCenter.email,
        ServiceCenter.address,
        ServiceCenter.is_active,
    ]
    name = "сервисный центр"
    name_plural = "Сервисные центры"
    column_labels = {**get_column_comments(ServiceCenter)}
    column_formatters = {
        ServiceCenter.created_at: lambda m, _: to_moscow(m.created_at)}
    column_formatters_detail = column_formatters


class PartsRequestAdmin(ModelView, model=PartsRequest):
    """Административный интерфейс для модели PartsRequest."""
    column_list = [
        PartsRequest.id,
        PartsRequest.asc_id,
        PartsRequest.status,
        PartsRequest.is_urgent,
        PartsRequest.work_order_number,
        PartsRequest.device_model,
        PartsRequest.serial_number,
        PartsRequest.comment_asc,
    ]
    name = "запрос на запчасти"
    name_plural = "Запросы на запчасти"
    column_labels = {**get_column_comments(PartsRequest)}
    column_formatters = {
        PartsRequest.created_at: lambda m, _: to_moscow(m.created_at),
        PartsRequest.status: lambda obj, name: obj.status.value
    }
    column_formatters_detail = column_formatters

    form_args = {
        "status": {
            "choices": [
                (status.name, status.value)
                for status in RequestStatus
            ]
        }
    }
    form_overrides = {
        "status": SelectField,
    }
