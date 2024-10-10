from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_menu_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Установить", callback_data="install_guide_menu"),
    ],
    [
        InlineKeyboardButton(text="Оплатить", callback_data="go_pay"),
    ],
])

start_wref_menu_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Установить", callback_data="install_guide_menu"),
    ],
    [
        InlineKeyboardButton(text="Оплатить", callback_data="go_pay"),
    ],
    [
        InlineKeyboardButton(text="Реф код", callback_data="ref_code_cb"),
    ]
])

start_admin_menu_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Установить", callback_data="install_guide_menu"),
    ],
    [
        InlineKeyboardButton(text="Оплатить", callback_data="go_pay"),
    ],
    [
        InlineKeyboardButton(text="Реф код", callback_data="ref_code_cb"),
    ],
    [
        InlineKeyboardButton(text="Дать привилегии", callback_data="add_wref_cb"),
        InlineKeyboardButton(text="Забрать привилегии", callback_data="remove_wref_cb"),
    ],
    [
        InlineKeyboardButton(text="Убрать оплату", callback_data="remove_pay_cb"),
        InlineKeyboardButton(text="Сделать платным", callback_data="add_pay_cb"),
    ],
    [
        InlineKeyboardButton(text="Забанить", callback_data="ban_cb"),
        InlineKeyboardButton(text="Разбанить", callback_data="unban_cb"),
    ],
])