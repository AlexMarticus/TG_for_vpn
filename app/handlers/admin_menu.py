from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.data.config import ADMINS
from app.database import requests as rq
from app.middlewares.check_is_banned import CheckIsBannedMiddleware

from app.keyboards.all_users_kb import kb_all_users
from app.keyboards.start_menu import start_admin_menu_ikb


router = Router()
router.callback_query.outer_middleware(CheckIsBannedMiddleware())


@router.callback_query(F.data.in_({'add_wref_cb', 'remove_wref_cb', 'remove_pay_cb', 'add_pay_cb', 'ban_cb', 'unban_cb'}))
async def show_users(callback: CallbackQuery):
    if callback.from_user.id in ADMINS:
        await callback.message.edit_text('Выберите пользователя', reply_markup=await kb_all_users(callback.data))


@router.callback_query(F.data.startswith('users__'))
async def is_change_user_permissions(callback: CallbackQuery):
    if callback.from_user.id in ADMINS:
        user_id, command = callback.data.split('__')[1:]
        user = await rq.info_user(user_id=user_id)
        menu_ikb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data=f"yes__{user_id}__{command}__{user.tg_id}"),
            ],
            [
                InlineKeyboardButton(text="В главное меню", callback_data="to_main"),
            ],
        ])
        user_came_from = await rq.came_from(user_id)
        await callback.message.edit_text(f"Telegram ID: {user.tg_id}\nTelegram username: @{user.username}\nПочта: "
                                         f"{user.email}\nИмя: {user.name}\nПлатит? {not user.is_without_payment}\n"
                                         f"Даёт рефы? {user.can_make_ref}\nЗабанен? {user.is_banned}\n{"-"*7}\n"
                                         f"Пришёл от:\n"
                                         f"Telegram ID: {user_came_from.tg_id}\nTelegram username: "
                                         f"@{user_came_from.username}\nПочта: {user_came_from.email}\n"
                                         f"Имя: {user_came_from.name}\nПлатит? {not user_came_from.is_without_payment}\n"
                                         f"Даёт рефы? {user_came_from.can_make_ref}\n"
                                         f"Забанен? {user_came_from.is_banned}\n"
                                         f"{"-" * 7}\n", reply_markup=menu_ikb)


@router.callback_query(F.data.startswith('yes__'))
async def change_user_permissions(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id in ADMINS:
        user_id, command, tg_id = callback.data.split('__')[1:]
        if command == 'add_wref_cb':
            message = 'Вам выдали привилегии'
            await rq.can_take_ref(user_id=user_id, is_can=True)
        elif command == 'remove_wref_cb':
            message = 'Вас лишили привилегий'
            await rq.can_take_ref(user_id=user_id, is_can=False)
        elif command == 'remove_pay_cb':
            message = 'Для вас ВПН теперь бесплатный'
            await rq.can_no_pay(user_id=user_id, is_can=True)
        elif command == 'add_pay_cb':
            message = 'Для вас ВПН теперь снова платный'
            await rq.can_no_pay(user_id=user_id, is_can=False)
            await rq.refresh_date_next_pay(user_id=user_id, is_was_wout_pay=True)
        elif command == 'ban_cb':
            message = 'Вас забанили'
            await rq.ban_unban(user_id=user_id, is_ban=True)
        else:
            message = 'Вас разбанили'
            await rq.ban_unban(user_id=user_id, is_ban=False)
        await bot.send_message(chat_id=tg_id, text=message)
        await callback.message.edit_text('Сделано', reply_markup=start_admin_menu_ikb)
