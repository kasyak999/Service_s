from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import (
    declarative_base, declared_attr, mapped_column, Mapped
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0),
        nullable=False,
        comment='Дата создания',
    )


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
