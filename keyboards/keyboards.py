from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from lexicon.lexicon_en import MAIN_LEXICON, ACCOUNT_SETTINGS


# YES | NO Buttons

button_yes: KeyboardButton = KeyboardButton(text=MAIN_LEXICON['YES'])
button_no: KeyboardButton = KeyboardButton(text=MAIN_LEXICON['NO'])

YES_NO_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[button_yes, button_no],
                                                           one_time_keyboard=True,
                                                           resize_keyboard=True)

# OPTION SELECTION

button_old: KeyboardButton = KeyboardButton(text=MAIN_LEXICON['OLD'])
button_new: KeyboardButton = KeyboardButton(text=MAIN_LEXICON['NEW'])
button_options: KeyboardButton = KeyboardButton(text=MAIN_LEXICON['OPTIONS'])

MAIN_MENU_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[button_old, button_new, button_options],
                                                              one_time_keyboard=True,
                                                              resize_keyboard=True)

# WORDS AMOUNT SELECTION

AMOUNT_SELECTION_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[i for i in range(10, 40, 5)],
                                                                     one_time_keyboard=True,
                                                                     resize_keyboard=True)

# SETTINGS KEYBOARD

USER_BUTTON: KeyboardButton = KeyboardButton(text=ACCOUNT_SETTINGS['USER'])
LIBRARY_BUTTON: KeyboardButton = KeyboardButton(text=ACCOUNT_SETTINGS['LIBRARY'])


MAIN_OPTIONS_PAGE_LIBRARY: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[USER_BUTTON, LIBRARY_BUTTON],
                                                                     one_time_keyboard=True,
                                                                     resize_keyboard=True)
