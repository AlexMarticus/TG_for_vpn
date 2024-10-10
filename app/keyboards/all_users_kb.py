from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data.config import ADMINS
from app.database.requests import get_all_users


async def kb_all_users(command):
    users = await get_all_users()
    keyboard = InlineKeyboardBuilder()
    for user in users:
        if user.tg_id not in ADMINS:
            show_text = user.username if user.username else user.tg_id
            if command == 'unban_cb':
                if user.is_banned:
                    keyboard.add(InlineKeyboardButton(text=f"{show_text}", callback_data=f'users__{user.id}__{command}'))
            elif command == 'ban_cb':
                if not user.is_banned:
                    keyboard.add(InlineKeyboardButton(text=f"{show_text}", callback_data=f'users__{user.id}__{command}'))
            else:
                keyboard.add(InlineKeyboardButton(text=f"{show_text}", callback_data=f'users__{user.id}__{command}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()