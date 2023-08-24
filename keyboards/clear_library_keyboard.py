from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_en import MAIN_LEXICON


# cancel keyboard
CANCEL_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=MAIN_LEXICON['CANCEL'],
                                                           callback_data='cancel')

CANCEL_K_B: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[CANCEL_BUTTON]])
