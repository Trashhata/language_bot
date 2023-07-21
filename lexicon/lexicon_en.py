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
    '/start': 'Welcome to the word learning bot!',
    '/beginning': 'To the main menu.',
    '/help': 'Bot help.'
}

REGISTRATION: dict[str: str] = {
    'INITIALIZATION': 'Please enter your name.',
    'INCORRECT_NAME': 'The name must contain only letters.',
    'AGE_ENTER': 'Enter your age.',
    'INCORRECT_AGE': 'Age must be a number from 5 to 110.',
    'AVATAR_SELECTION': 'Please select avatar image or press skip button.',
    'INCORRECT_DATA': 'The avatar must be an image.'
}

LESSON_LEXICON: dict[str: str] = {
    'AMOUNT_SELECTION': 'Please select number of learning words in the keyboard below:',
    'ONCE_MORE': 'Would you like to have another lesson?'
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