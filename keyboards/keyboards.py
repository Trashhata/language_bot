from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from lexicon.lang_selection import get_phrase


# YES | NO Buttons
async def yes_no_k_b(user_id: int):

    button_yes: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'YES'))
    button_no: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'NO'))

    return ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]],
                               one_time_keyboard=True,
                               resize_keyboard=True)


# OPTION SELECTION
async def option_k_b(user_id: int):
    button_old: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'OLD'))
    button_new: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'NEW'))
    button_options: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'OPTIONS'))

    return ReplyKeyboardMarkup(keyboard=[[button_old, button_new, button_options]],
                               one_time_keyboard=True,
                               resize_keyboard=True)


# SETTINGS KEYBOARD
async def settings_k_b(user_id: int):
    user_button: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'USER'))
    library_button: KeyboardButton = KeyboardButton(text=get_phrase(user_id, 'LIBRARY'))

    return ReplyKeyboardMarkup(keyboard=[(user_button, library_button)],
                               one_time_keyboard=True,
                               resize_keyboard=True)


# SKIP KEYBOARD
async def skip_k_b(user_id: int):
    skip_button: InlineKeyboardButton = InlineKeyboardButton(text=get_phrase(user_id, 'SKIP'),
                                                             callback_data='Skip.')

    return InlineKeyboardMarkup(inline_keyboard=[[skip_button]])


class LanguageCustomCallback(CallbackData, prefix='lang'):
    lang: str
    data: str = 'language'


# LANGUAGE SELECTION KEYBOARD
async def language_select_k_b(user_id: int):
    ru_button: InlineKeyboardButton = InlineKeyboardButton(text=get_phrase(user_id, 'RU'),
                                                           callback_data=LanguageCustomCallback(lang='ru').pack())

    en_button: InlineKeyboardButton = InlineKeyboardButton(text=get_phrase(user_id, 'EN'),
                                                           callback_data=LanguageCustomCallback(lang='en').pack())

    return InlineKeyboardMarkup(inline_keyboard=[[ru_button, en_button]])
