MAIN_LEXICON: dict[str: str] = {
    'YES': 'Yes',
    'NO': 'No',
    'SKIP': 'Skip',
    'WELCOME': "Welcome! I'm a word learning bot. Please select one of existing options and have fun!",
    'OPTIONS': 'Account settings',
    'NEW': 'New words',
    'OLD': 'Repetition'
}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Getting started',
    '/new_lesson': 'Start the new lesson.',
    '/repetition': 'Old words repetition.',
    '/settings': 'User information and words control.',
    '/help': 'Bot help.'
}

MAIN_MENU_LEXICON: dict[str, str] = {
    'START_MESSAGE': '''Welcome to the word learning bot!
To start new lesson push /new_lesson
To start repetition push /repetition
To enter setting push /setting
For help push /help''',
    'HELP_MESSAGE': '''This bot was created for a language learning.
Tap "new lesson" command for learning new words.
Tap "repetition" command for old words repetition.
To enter settings tap "settings" command.''',
    'LESSON_START': 'Starting the new lesson.',
    'SETTINGS_DESCR': 'Here you can change user information\nand control word base.'
}

REGISTRATION: dict[str: str] = {
    'INITIALIZATION': 'Please enter your name.',
    'INCORRECT_NAME': 'The name must contain only letters.',
    'AGE_ENTER': 'Enter your age.',
    'INCORRECT_AGE': 'Age must be a number from 5 to 110.',
    'AVATAR_SELECTION': 'Please select avatar image or press skip button.',
    'SKIP': 'Skip',
    'TAP_TO_SKIP': 'Tap me!',
    'INCORRECT_DATA': 'The avatar must be an image.',
    'REGISTRATION_FINISHED': 'Successful registration.'
}

LESSON_LEXICON: dict[str: str] = {
    'AMOUNT_SELECTION': 'Please select number of learning words in the keyboard below:',
    'INCORRECT_AMOUNT': 'Amount must be a number from 10 to 40.',
    'LESSON_IS_OVER': 'Lesson is over.\nWould you like to have another lesson?',
    'LESSON_STARTING': 'Please wait, lesson is starting...',
    'RIGHT_ANSWER': 'Right answer!',
    'INCORRECT_ANSWER': 'Incorrect answer! The right answer is: '

}

ACCOUNT_SETTINGS: dict[str: dict | str] = {
    'USER': 'User information settings',
    'USER_INFORMATION': {'INITIALIZATION': 'Which information would you like to change?',
                         'NAME': 'Name.',
                         'AGE': 'Age.',
                         'AVATAR': 'Avatar.',
                         'DELETE': 'Delete profile.',
                         'CONFIRMATION': 'Enter "DELETE PROFILE" to confirm.',
                         'SUCCESS': 'Profile deleted.'},
    'LIBRARY': 'Words library settings',
    'WORD_LIBRARY': {'EDIT': 'Edit word library.',
                     'WEB_PAGE': 'Open Wiki Dictionary page.',
                     'DELETE': 'Delete.',
                     'MARK': 'Mark/unamark as learned.',
                     'CLEAR': 'Clear library.',
                     'CONFIRMATION': 'Enter "CLEAR LIBRARY" to confirm.',
                     'SUCCESS': 'Library cleaned.',
                     'NEXT': '>>',
                     'PREV': '<<'
                     }
}