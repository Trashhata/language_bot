from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon_en import ACCOUNT_SETTINGS, MAIN_LEXICON


# class for userinfo menu callback
class UserInfoChangeCallback(CallbackData, prefix='user_info'):
    flag: str
    option: str


BACK_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=MAIN_LEXICON['BACK'],
                                                         callback_data='back')

# options main menu keyboard
USER_INFO_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['USER'],
                                                              callback_data='user_info')
WORD_LIBRARY_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['LIBRARY'],
                                                                 callback_data='library')

MAIN_OPTIONS_MENU_KB: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[USER_INFO_BUTTON,
                                                                                    WORD_LIBRARY_BUTTON]])

# user information settings menu
NAME_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['USER_INFORMATION']['NAME'],
                                                         callback_data=UserInfoChangeCallback(flag='user_info_change',
                                                                                              option='name').pack())

AGE_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['USER_INFORMATION']['AGE'],
                                                        callback_data=UserInfoChangeCallback(flag='user_info_change',
                                                                                             option='age').pack())

AVATAR_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['USER_INFORMATION']['AVATAR'],
                                                           callback_data=UserInfoChangeCallback(flag='user_info_change',
                                                                                                option='photo').pack())

DELETE_USER_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['USER_INFORMATION']['DELETE'],
                                                                callback_data='delete')

USER_INFO_K_b: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[NAME_BUTTON],
                                                                            [AGE_BUTTON],
                                                                            [AVATAR_BUTTON],
                                                                            [DELETE_USER_BUTTON],
                                                                            [BACK_BUTTON]])
