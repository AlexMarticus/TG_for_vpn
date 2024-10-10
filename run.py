import asyncio
import logging
from datetime import timedelta, datetime

from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.database.requests import get_all_users, ban_unban
from app.handlers import (admin_menu, commands, different_handlers, funny_handler, install_guide, paying,
                          ref_code_handler, registration)
from app.data.config import BOT_TOKEN, ADMINS, DB_NAME, MY_PHONE
from app.database.models import async_main


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def send_monthly_message():
    users = await get_all_users()
    for user in users:
        if user.date_next_pay is not None:
            if (user.date_next_pay - timedelta(days=3) <= datetime.now() and not user.is_banned and
                    not user.is_without_payment):
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Проверить оплату", callback_data=f"i_paied__{user.id}__{user.tg_id}"),
                    ],
                ])
                await bot.send_message(chat_id=user.tg_id, text=f"Напоминание об оплате:\n{MY_PHONE}\nТ Банк или Сбер\n"
                                                                "В комментариях укажите свой телеграм",
                                       reply_markup=keyboard, parse_mode='MARKDOWN')
            if user.date_next_pay >= datetime.now() + timedelta(days=3):
                await ban_unban(user_id=user.id, is_ban=True)
    # и отправка бд мне в тг для архивации
    await bot.send_document(chat_id=ADMINS[0], document=DB_NAME)


def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_monthly_message, CronTrigger(hour='10', minute='00'))
    scheduler.start()
    print('Планировщик запущен')


async def main():
    setup_scheduler()
    await async_main()
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(admin_menu.router, commands.router, different_handlers.router, funny_handler.router,
                       install_guide.router, paying.router, ref_code_handler.router, registration.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')