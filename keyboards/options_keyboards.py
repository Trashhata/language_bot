from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from lexicon.lang_selection import get_phrase


# class for userinfo menu callback
class UserInfoChangeCallback(CallbackData, prefix='user_info'):
    flag: str
    option: str


# options menu keyboard
async def options_k_b(user_id: int):
    user_info_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'USER'),
                                                                  callback_data='user_info')
    world_library_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'LIBRARY'),
                                                                      callback_data='library')

    language_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'LANGUAGE'),
                                                                 callback_data='language')

    return InlineKeyboardMarkup(inline_keyboard=[[user_info_button],
                                                 [world_library_button],
                                                 [language_button]])


# user information settings menu
async def info_settings_k_b(user_id: int):
    name_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'NAME'),
                                                             callback_data=UserInfoChangeCallback(
                                                                 flag='user_info_change',
                                                                 option='name').pack())

    age_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'AGE'),
                                                            callback_data=UserInfoChangeCallback(
                                                                flag='user_info_change',
                                                                option='age').pack())

    avatar_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'AVATAR'),
                                                               callback_data=UserInfoChangeCallback(
                                                                   flag='user_info_change',
                                                                   option='photo').pack())

    back_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'BACK'),
                                                             callback_data='back')

    return InlineKeyboardMarkup(inline_keyboard=[[name_button],
                                                 [age_button],
                                                 [avatar_button],
                                                 [back_button]])


class LanguageCustomCallback(CallbackData, prefix='lang_change'):
    lang: str
    flag: str = 'lang'


# keyboard for a language setting menu
async def language_change_k_b(user_id: int):
    ru_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'RU'),
                                                           callback_data=LanguageCustomCallback(lang='ru').pack())

    en_button: InlineKeyboardButton = InlineKeyboardButton(text=await get_phrase(user_id, 'EN'),
                                                           callback_data=LanguageCustomCallback(lang='en').pack())

    return InlineKeyboardMarkup(inline_keyboard=[[ru_button, en_button]])
