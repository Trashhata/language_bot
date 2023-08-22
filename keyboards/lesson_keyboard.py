from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon_en import LESSON_LEXICON
from random import shuffle


class AmountCallback(CallbackData, prefix='amount'):
    flag: str
    amount: int


# WORDS AMOUNT SELECTION
AMOUNT_SELECTION_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(i), callback_data=AmountCallback(flag='amount', amount=i).pack()) for i in (10, 15, 20)],
                                                                                        [InlineKeyboardButton(text=str(i), callback_data=AmountCallback(flag='amount', amount=i).pack()) for i in (25, 30, 35)],
                                                                                        [InlineKeyboardButton(text=str(i), callback_data=AmountCallback(flag='amount', amount=i).pack()) for i in (40,)]])


# keyboard with answer options
def choice_keyboard_creation(choices) -> InlineKeyboardMarkup:
    answers: list[str] = [choices.right_answer.translation] + [i.translation for i in choices.other_answers]
    shuffle(answers)

    choice_keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for word in answers:
        callback = 'True' if choices.right_answer.translation == word else 'False'

        choice_keyboard.add(InlineKeyboardButton(text=word,
                                                 callback_data=callback))

    choice_keyboard.adjust(1)

    return choice_keyboard.as_markup()


# keyboard for lesson repeating
def repeat_lesson_or_not() -> InlineKeyboardMarkup:
    repeat_button: InlineKeyboardButton = InlineKeyboardButton(text=LESSON_LEXICON['REPEAT_LESSON'],
                                                               callback_data='repeat')

    finish_button: InlineKeyboardButton = InlineKeyboardButton(text=LESSON_LEXICON['FINISH_LESSON'],
                                                               callback_data='finish')

    k_b: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[repeat_button, finish_button]])

    return k_b
