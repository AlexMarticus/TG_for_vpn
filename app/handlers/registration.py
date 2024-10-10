from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.keyboards.start_menu import start_menu_ikb
from app.database import requests as rq
from app.utils.distr import update_json, restart_xray
from app.middlewares.check_is_banned import CheckIsBannedMiddleware
from app.states.registration import Registration
from app.data.config import ADMINS
from aiogram import Router


router = Router()
router.message.outer_middleware(CheckIsBannedMiddleware())


@router.message(Registration.ref_code)
async def reg_ref_code(message: Message, state: FSMContext):
    ref_id = await rq.check_ref(message.text)
    if ref_id != -1 or message.from_user.id in ADMINS:
        await state.update_data(ref_id=ref_id)
        await state.set_state(Registration.name)
        await message.answer('Введите имя (для отображения человеку, кто поделился кодом)')
    else:
        await message.answer('Реферальный код введен неверно. Попробуйте еще раз')
        await state.set_state(Registration.ref_code)


@router.message(Registration.name)
async def reg_name(message: Message, state: FSMContext):
    if len(message.text) < 30:
        await state.update_data(name=message.text)
        await state.set_state(Registration.email)
        await message.answer('Введите свою почту')
    else:
        await state.set_state(Registration.name)
        await message.answer('Слишком длинное имя. Максимум 30 символов. Попробуйте еще раз')


@router.message(Registration.email)
async def reg_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Registration.again)
    await message.delete()
    await message.answer('Введите свою почту еще раз')


@router.message(Registration.again)
async def reg_email_again(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['email'] == message.text:
        await message.delete()
        client_id = await rq.get_client_id()
        await rq.add_user(tg_id=message.from_user.id, email=data['email'], client_id=client_id, name=data['name'],
                          username=message.from_user.username if message.from_user.username else None)
        await rq.update_ref(refcode_id=data['ref_id'], user_id=(await rq.info_user(tg_id=message.from_user.id)).id)
        await update_json(client_id=client_id, email=data['email'], tg_id=message.from_user.id)
        await restart_xray()
        await message.answer('Регистрация завершена успешно', reply_markup=start_menu_ikb)
        await state.clear()
    else:
        await message.delete()
        await message.answer('Введеные почты не совпадают. Попробуйте еще раз')
        await state.set_state(Registration.email)
