from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards import start_menu as kb
from app.database import requests as rq
from app.middlewares.check_is_banned import CheckIsBannedMiddleware
from app.states.registration import Registration
from app.data.config import ADMINS, MY_EMAIL, MY_CLIENT_ID, MY_NAME, MY_USERNAME
from aiogram import Router


router = Router()
router.message.outer_middleware(CheckIsBannedMiddleware())


@router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    if not await rq.is_user_regged(message.from_user.id):
        if message.from_user.id in ADMINS:
            await rq.add_user(tg_id=message.from_user.id, email=MY_EMAIL,
                              client_id=MY_CLIENT_ID, name=MY_NAME,
                              username=message.from_user.username if message.from_user.username else None)
        await message.answer('Введите реферальный код')
        await state.set_state(Registration.ref_code)
    elif await rq.is_user_admin(message.from_user.id):
        await message.answer(f"Привет, админ", reply_markup=kb.start_admin_menu_ikb)
    elif await rq.is_can_make_ref(message.from_user.id):
        await message.answer('Привет, привилегированный друг ;)', reply_markup=kb.start_wref_menu_ikb)
    else:
        await message.answer(f"Привет", reply_markup=kb.start_menu_ikb)


@router.message(Command('help'))
async def bot_help(message: Message):
    await message.answer(f"По техническим вопросам писать: @{MY_USERNAME}")
