from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon_en import ACCOUNT_SETTINGS

from external_services.get_random_word import Word
from services.word_library_services import world_library_page
from data_base.sqlite_base import get_from_base


# callback for marking word as learned or not learned
class CustomCallbackWordLearned(CallbackData, prefix='word_edit'):
    word: str
    option: bool
    current_page: int
    data: str = 'learned_mark'


# callback for a word deleting
class CustomCallbackWordDelete(CallbackData, prefix='word_del'):
    word: str
    current_page: int
    option: str = 'delete'


class CustomCallbackTurnPage(CallbackData, prefix='turn_page'):
    page_num: int | str
    option: str = 'turn_page'


# library settings menu
EDIT_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['EDIT'],
                                                         callback_data='edit_library')

CLEAR_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['CLEAR'],
                                                          callback_data='clear_library')

ADD_WORD_BUTTON: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['ADD'],
                                                             callback_data='new_word')

LIBRARY_MAIN_K_B: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[EDIT_BUTTON],
                                                                               [CLEAR_BUTTON],
                                                                               [ADD_WORD_BUTTON]],)


# generates page of user word library
async def generate_library_page(user_id: int, page: int) -> InlineKeyboardMarkup | bool:
    words: list[Word] = await world_library_page(user_id, page)

    markup: list[list[InlineKeyboardButton]] = []

    # each row (word, translation, learned/not learned), delete button below
    for word in words:
        word_button: InlineKeyboardButton = InlineKeyboardButton(text=word.word,
                                                                 callback_data='pass')
        word_translation: InlineKeyboardButton = InlineKeyboardButton(text=word.translation.split(',')[0],
                                                                      callback_data='pass')
        if word.learned:
            learned, learned_callback_data = ACCOUNT_SETTINGS['WORD_LIBRARY']['LEARNED'], False
        else:
            learned, learned_callback_data = ACCOUNT_SETTINGS['WORD_LIBRARY']['NOT_LEARNED'], True

        c_b: CustomCallbackWordLearned = CustomCallbackWordLearned(word=word.word,
                                                                   option=learned_callback_data,
                                                                   current_page=page)

        learned_button: InlineKeyboardButton = InlineKeyboardButton(text=learned, callback_data=c_b.pack())
        delete_button: InlineKeyboardButton = InlineKeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['DELETE'],
                                                                   callback_data=CustomCallbackWordDelete(
                                                                       word=word.word,
                                                                       current_page=page
                                                                   ).pack())

        markup.append([word_button, word_translation])
        markup.append([learned_button, delete_button])

    # check for first page
    if page > 1:
        prev_button = InlineKeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['PREV'],
                                           callback_data=CustomCallbackTurnPage(page_num=page - 1).pack())
    else:
        prev_button = InlineKeyboardButton(text='',
                                           callback_data='pass')

    # check for last page
    if len((await get_from_base(user_id)).words) - page * 7 < 0:
        next_button = InlineKeyboardButton(text='',
                                           callback_data='pass')
    else:
        next_button = InlineKeyboardButton(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['NEXT'],
                                           callback_data=CustomCallbackTurnPage(page_num=page + 1).pack())

    current_page_button = InlineKeyboardButton(text=f'Page {page}', callback_data='pass')

    # the last row with pagination
    markup.append([prev_button, current_page_button, next_button])

    current_page_k_b: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=markup)

    return current_page_k_b
