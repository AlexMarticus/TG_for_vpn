import calendar
from datetime import datetime, timedelta

from app.database.models import async_session
from app.database.models import User, RefCode
from sqlalchemy import select

from app.utils.distr import get_client_id
from app.data.config import ADMINS


async def is_user_regged(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return True
        return False


async def is_user_banned(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user and user.is_banned:
            return True
        return False


async def can_take_ref(user_id, is_can):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        user.can_make_ref = is_can
        await session.commit()


async def can_no_pay(user_id, is_can):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        user.is_without_payment = is_can
        await session.commit()


async def ban_unban(user_id, is_ban):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        user.is_banned = is_ban
        await session.commit()


async def came_from(user_id) -> User:
    async with async_session() as session:
        refcode_info = await session.scalar(select(RefCode).where(RefCode.child == user_id))
        return await session.scalar(select(User).where(User.id == refcode_info.parent))


async def info_user(user_id=None, tg_id=None) -> User:
    async with async_session() as session:
        if user_id:
            user = await session.scalar(select(User).where(User.id == user_id))
        else:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def refresh_date_next_pay(user_id, is_was_wout_pay=False):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user.date_next_pay is None or is_was_wout_pay:
            user.date_next_pay = datetime.now() + timedelta(days=1)
        else:
            days = calendar.monthrange(user.date_next_pay.year, user.date_next_pay.month)[1]
            user.date_next_pay = user.date_next_pay + timedelta(days=days)
        await session.commit()


async def check_ref(refcode):
    async with async_session() as session:
        refcode_info = await session.scalar(select(RefCode).where(RefCode.refcode == refcode))
        if refcode_info:
            parent, ref_id = refcode_info.parent, refcode_info.id
            refcode_info.child = 1 # Заглушка. Потом обновим (update_ref)
            await session.commit()
            await get_free_ref(parent)
            return ref_id
        else:
            return -1


async def update_ref(refcode_id, user_id):
    async with async_session() as session:
        refcode_info = await session.scalar(select(RefCode).where(RefCode.id == refcode_id))
        refcode_info.child = user_id
        await session.commit()


async def get_free_ref(user_id):
    async with async_session() as session:
        refcode_info = await session.scalar(select(RefCode).where(RefCode.child == None))
        if refcode_info:
            refcode = refcode_info.refcode
        else:
            refcode = await get_client_id()
            session.add(RefCode(parent=user_id, refcode=refcode))
            await session.commit()
        return refcode


async def get_all_users() -> list:
    async with async_session() as session:
        return await session.scalars(select(User))


async def is_can_make_ref(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user and user.can_make_ref:
            return True
        return False


async def is_user_admin(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user and user.is_admin:
            return True
        return False


async def add_user(tg_id, email, client_id, name, username=None):
    async with async_session() as session:
        is_admin = False
        if tg_id in ADMINS:
            is_admin = True
        session.add(User(tg_id=tg_id, email=email, client_id=client_id, name=name, username=username, is_admin=is_admin))
        await session.commit()
