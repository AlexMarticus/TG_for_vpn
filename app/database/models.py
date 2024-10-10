from datetime import datetime

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.data.config import DB_NAME

engine = create_async_engine(url=f'sqlite+aiosqlite:///{DB_NAME}')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    can_make_ref: Mapped[bool] = mapped_column(default=False)

    client_id: Mapped[str] = mapped_column(String(36))
    date_get_client_id: Mapped[datetime] = mapped_column(server_default=func.now())

    is_without_payment: Mapped[bool] = mapped_column(default=False)
    date_next_pay: Mapped[datetime] = mapped_column(nullable=True)

    is_banned: Mapped[bool] = mapped_column(default=False)
    date_ban: Mapped[datetime] = mapped_column(nullable=True)


class RefCode(Base):
    __tablename__ = 'ref_code'

    id: Mapped[int] = mapped_column(primary_key=True)
    refcode: Mapped[str] = mapped_column(String(36), unique=True)
    parent: Mapped[int] = mapped_column(ForeignKey('users.id'))
    child: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

