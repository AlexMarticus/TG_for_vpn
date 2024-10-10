from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.database import requests as rq
from app.middlewares.check_is_banned import CheckIsBannedMiddleware
from app.data.config import ADMINS

router = Router()
router.message.outer_middleware(CheckIsBannedMiddleware())


@router.callback_query(F.data=='go_pay')
async def pay_menu(callback: CallbackQuery):
    user = await rq.info_user(tg_id=callback.from_user.id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="В главное меню", callback_data="to_main"),
        ],
    ])
    if user.date_next_pay is None:
        await rq.refresh_date_next_pay(user_id=user.id)
    if user.is_without_payment:
        await callback.message.edit_text('Для вас ВПН бесплатный', reply_markup=keyboard)
    else:
        await callback.message.edit_text(f'ВПН стоит 55 рублей в месяц\n\nСледующая оплата: '
                                         f'{user.date_next_pay.strftime("%d %B %Y")}\n'
                                         f'Мы пришлем вам напоминание', reply_markup=keyboard)


@router.callback_query(F.data.startswith('i_paied__'))
async def check_paying(callback: CallbackQuery, bot: Bot):
    user_id, tg_id = callback.data.split('__')[1:]
    text = f'Проверьте оплату от {tg_id}'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data=f"paied__yes__{user_id}__{tg_id}"),
        ],
        [
            InlineKeyboardButton(text="Нет", callback_data=f"paied_no__{user_id}__{tg_id}"),
        ],
    ])
    await bot.send_message(chat_id=ADMINS[0], text=text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('paied__'))
async def check_paying(callback: CallbackQuery, bot: Bot):
    res, user_id, tg_id = callback.data.split('__')[1:]
    if res == 'yes':
        await rq.refresh_date_next_pay(user_id=user_id)
        await bot.send_message(chat_id=tg_id, text='Оплата подтверждена')
    else:
        await bot.send_message(chat_id=tg_id, text='Оплата НЕ подтверждена')
    await callback.message.edit_text('Готово')