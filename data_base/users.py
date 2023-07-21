from external_services.get_info import get_info


class WordExistError(Exception):
    pass


# USER CLASS
class User:
    def __init__(self, name, age, photo):
        self.__name = name
        self.__age = age
        self.__photo = photo
        self.__words: dict[str, dict] = dict()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, new_age):
        self.__age = new_age

    @property
    def photo(self):
        return self.__photo

    @photo.setter
    def photo(self, new_photo):
        self.__photo = new_photo

    @property
    def words(self) -> iter:
        return iter((word, info) for word, info in sorted(self.__words.items()))

    def add_word(self, addable: str):
        if not self.__words.get(addable):
            self.__words[addable] = get_info()
            return True
        else:
            raise WordExistError('Word already in base.')

    def del_word(self, delitable: str):
        try:
            self.__words.pop(delitable)
            return True
        except KeyError:
            raise WordExistError("Word doesn't exist.")

    def learned(self, word: str, learned: bool):
        try:
            self.__words[word]['learned'] = learned
        except KeyError:
            raise WordExistError("Word doesn't exist.")

    def get_wiki(self, word: str):
        try:
            return self.__words[word]['wiki']
        except KeyError:
            raise WordExistError("Word doesn't exist.")


USER_BASE: dict[int, User] = {}
