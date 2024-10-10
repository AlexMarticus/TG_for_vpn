from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == 'Веня лох')
async def say_yes(message: Message):
    await message.answer('Согласен!')
