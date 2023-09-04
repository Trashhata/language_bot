from aiogram import Router, F
from aiogram.types import Message

from lexicon.lang_selection import get_phrase


router: Router = Router()


# handler for any unsupported messages
@router.message()
async def unsupported_command(message: Message):
    await message.answer(f'"{message.text}"' + await get_phrase(message.from_user.id, 'UNSUPPORTED'))


@router.callback_query(F.data == 'pass')
async def pass_callback(*args, **kwargs):
    pass
