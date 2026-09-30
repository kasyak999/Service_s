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
        ServiceCenter.user,
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
        ServiceCenter.created_at: lambda m, _: to_moscow(m.created_at),
        ServiceCenter.address: lambda m, _: (
            m.address[:30] + "..."
            if m.address and len(m.address) > 30 else m.address
        ),
    }
    column_formatters_detail = column_formatters


class PartsRequestAdmin(ModelView, model=PartsRequest):
    """Административный интерфейс для модели PartsRequest."""
    column_list = [
        PartsRequest.asc,
        PartsRequest.status,
        PartsRequest.is_urgent,
        PartsRequest.created_at,
        PartsRequest.work_order_number,
        PartsRequest.device_model,
        PartsRequest.comment_asc,
    ]
    name = "запрос на запчасти"
    name_plural = "Запросы на запчасти"
    column_labels = {**get_column_comments(PartsRequest)}
    column_formatters = {
        PartsRequest.created_at: lambda m, _: to_moscow(m.created_at),
        PartsRequest.status: lambda obj, name: obj.status.value,
        PartsRequest.comment_asc: lambda m, _: (
                m.comment_asc[:30] + "..."
                if m.comment_asc and len(m.comment_asc) > 30 else m.comment_asc
            ),
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
