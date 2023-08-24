from aiogram import Router, F
from aiogram.types import Message


router: Router = Router()


# handler for any unsupported messages
@router.message()
async def unsupported_command(message: Message):
    await message.answer(f'"{message.text}" is unsupported command.')


@router.callback_query(F.data == 'pass')
async def pass_callback(*args, **kwargs):
    pass
