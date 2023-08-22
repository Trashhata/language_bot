from aiogram.types import Message


def age_filter(message: Message):
    return message.text.isdigit() and 5 <= int(message.text) <= 110
