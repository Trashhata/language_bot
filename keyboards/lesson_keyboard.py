from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from random import shuffle

# WORDS AMOUNT SELECTION
AMOUNT_SELECTION_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(i)) for i in (10, 15, 20)],
                                                                               [KeyboardButton(text=str(i)) for i in (25, 30, 35)],
                                                                               [KeyboardButton(text=str(i)) for i in (40,)]],
                                                                     one_time_keyboard=True,
                                                                     resize_keyboard=True)


def choice_keyboard_creation(choices) -> InlineKeyboardMarkup:
    answers: list[str] = [choices.right_answer.translation] + [i.translation for i in choices.other_answers]
    shuffle(answers)

    choice_keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for word in answers:
        callback = 'True' if choices.right_answer.translation == word else 'False'

        choice_keyboard.add(InlineKeyboardButton(text=word,
                                                 callback_data=callback))

    return choice_keyboard.as_markup()
