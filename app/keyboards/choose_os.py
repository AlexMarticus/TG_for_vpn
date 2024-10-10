from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

install_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Android', callback_data="install_android"),
        InlineKeyboardButton(text='IOS', callback_data="install_ios"),
    ],
    [
        InlineKeyboardButton(text='Windows', callback_data="install_windows"),
        InlineKeyboardButton(text='MacOS', callback_data="install_macos"),
        InlineKeyboardButton(text='Linux', callback_data="install_linux"),
    ],
    [
        InlineKeyboardButton(text='В главное меню', callback_data="to_main"),
    ]
])
