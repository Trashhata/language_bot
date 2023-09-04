import os


def open_file_in_same_directory(file_name: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, file_name)


# returns dict an object for reading
def get_dictionary(language: str = 'en-ru'):
    # commands: dict[str, str] = {'en-ru': '.'}

    return open(open_file_in_same_directory('eng_dictionary.csv'), 'r', encoding='windows-1251')
