from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.database import requests as rq
from app.keyboards.choose_os import install_ikb
from app.middlewares.check_is_banned import CheckIsBannedMiddleware


router = Router()
router.callback_query.outer_middleware(CheckIsBannedMiddleware())


@router.callback_query(F.data == 'install_guide_menu')
async def install_guide_menu(callback: CallbackQuery):
    await callback.answer('Выбрано: установка')
    user = await rq.info_user(tg_id=callback.from_user.id)
    if user.date_next_pay is None:
        await rq.refresh_date_next_pay(user_id=user.id)
    name = '-'.join(user.name)
    link1 = (f"vless://{user.client_id}@seerb.freemyip.com:443?security=tls&fp=chrome&type=tcp&flow=xtls-"
             f"rprx-vision&encryption=none#VLESS%20direct%20TLS%20{name}")
    link2 = (f"vless://{user.client_id}@seerb.freemyip.com:443?security=tls&fp=chrome&type=ws&path="
             f"/myverysecretpath&encryption=none#VLESS%20direct%20WEBS%20{name}")
    text = f"Необходимые вам ссылки:\n{'-'*10}\n`{link1}`\n{'-'*10}\n`{link2}`\n{'-'*10}\nВыберите устройство:"
    await callback.message.edit_text(text, reply_markup=install_ikb, parse_mode="MARKDOWN")


@router.callback_query(F.data=='install_android')
async def install_guide_android(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="install_guide_menu"),
        ],
    ])
    text = (f'Скачать: https://play.google.com/store/apps/details?id=com.v2ray.ang&hl=en_US\n'
            f'edit')
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data=='install_ios')
async def install_guide_ios(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="install_guide_menu"),
        ],
    ])
    text = (f'Скачать: https://apps.apple.com/us/app/foxray/id6448898396\n'
            f'edit')
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data=='install_windows')
async def install_guide_win(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="install_guide_menu"),
        ],
    ])
    text = (f'Скачать архив: https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-windows64.zip\n'
            f'Разархивировать и запустить')
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data=='install_linux')
async def install_guide_linux(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="install_guide_menu"),
        ],
    ])
    text = (f'Скачать архив: https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-linux64.zip\n'
            f'Разархивировать и запустить')
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data=='install_macos')
async def install_guide_macos(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="install_guide_menu"),
        ],
    ])
    text = f'EDIT'
    await callback.message.edit_text(text, reply_markup=keyboard)
