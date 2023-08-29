from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lang_selection import get_phrase


async def create_cancel_cb(user_id: int) -> InlineKeyboardMarkup:
    # cancel keyboard
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'CANCEL'),
                                                               callback_data='cancel')

    return InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
