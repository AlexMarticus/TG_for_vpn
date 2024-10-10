from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.data.config import BOT_USERNAME
from app.middlewares.check_is_banned import CheckIsBannedMiddleware
from app.database import requests as rq
from app.keyboards.start_menu import start_menu_ikb


router = Router()
router.callback_query.outer_middleware(CheckIsBannedMiddleware())


@router.callback_query(F.data == 'ref_code_cb')
async def get_ref_code(callback: CallbackQuery):
    if await rq.is_can_make_ref(callback.from_user.id) or await rq.is_user_admin(callback.from_user.id):
        await callback.answer('ПОСЛЕ КАЖДОГО ПРИГЛАШЕНИЯ КОД МЕНЯЕТСЯ')
        user = await rq.info_user(tg_id=callback.from_user.id)
        ref = await rq.get_free_ref(user.id)
        text = f"@{BOT_USERNAME}\nРеферальный код: <pre>{ref}</pre>"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="В главное меню", callback_data="to_main"),
            ],
        ])
        await callback.message.edit_text(text=text, reply_markup=markup, parse_mode="HTML")
    else:
        await callback.answer('Простите ;(')
        await callback.message.edit_text(text='Вас лишили привилегий ;(', reply_markup=start_menu_ikb)
