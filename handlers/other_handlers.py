from aiogram import Router
from aiogram.types import Message


router: Router = Router()


# handler for any unsupported messages
@router.message()
async def unsupported_command(message: Message):
    await message.answer(f'"{message.text}" is unsupported command.')