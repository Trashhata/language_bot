from aiogram import Router, F
from aiogram.types import Message

from lexicon.lang_selection import get_phrase


router: Router = Router()


# handler for any unsupported messages
@router.message()
async def unsupported_command(message: Message):
    try:
        await message.answer(f'"{message.text}"' + await get_phrase(message.from_user.id, 'UNSUPPORTED'))

    # if a user isn't registered and language can't be set up
    except TypeError:
        await message.answer(f'"{message.text}"' + await get_phrase(message.from_user.id, 'UNSUPPORTED',
                                                                    reg=True, reg_lang='ru'))


@router.callback_query(F.data == 'pass')
async def pass_callback(*args, **kwargs):
    pass
