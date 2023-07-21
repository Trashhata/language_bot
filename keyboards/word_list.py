from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from lexicon.lexicon_en import ACCOUNT_SETTINGS

from data_base.users import USER_BASE


# BUTTONS
PREV = KeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['PREV'])
NEXT = KeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['NEXT'])


def generate_keyboard(user_id: int):
    word_base: iter = USER_BASE[user_id].words
    finish = False

    table = []
    while not finish:
        current_keyboard: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
        for _ in range(25):
            try:
                word, info = word_base.next()
                current_keyboard.row(KeyboardButton(text=word),
                                     KeyboardButton(text=info['learned']),
                                     KeyboardButton(text=info['wiki_url']),
                                     KeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['DELETE']))
            except StopIteration:
                finish = True
                break

        current_keyboard.row(PREV, NEXT)

        table.append(current_keyboard)

    yield from table






