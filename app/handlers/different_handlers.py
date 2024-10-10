from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.middlewares.check_is_banned import CheckIsBannedMiddleware
from app.database import requests as rq
from app.keyboards import start_menu as kb

router = Router()
router.message.outer_middleware(CheckIsBannedMiddleware())


@router.callback_query(F.data == 'to_main')
async def go_to_main_menu(callback: CallbackQuery):
    if await rq.is_user_admin(callback.from_user.id):
        await callback.message.edit_text(f"Привет, админ", reply_markup=kb.start_admin_menu_ikb)
    elif await rq.is_can_make_ref(callback.from_user.id):
        await callback.message.edit_text('Привет, привилегированный друг ;)', reply_markup=kb.start_wref_menu_ikb)
    else:
        await callback.message.edit_text(f"Привет", reply_markup=kb.start_menu_ikb)
