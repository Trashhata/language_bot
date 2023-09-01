import aiosqlite
import pickle
from data_base.users import User


async def initiate_user_base():
    async with aiosqlite.connect('user_base.db') as db:
        await db.execute('create table if not exists UserBase (id int, user text, language text, UNIQUE(id, user, language))')

        await db.commit()


async def write_into_base(user_info: dict):
    async with aiosqlite.connect('user_base.db') as db:

        try:
            await db.execute(f"""
                INSERT INTO UserBase (id, user, language) 
                VALUES (?, ?, ?)
            """, (user_info['id'], pickle.dumps(User(user_info)), user_info['lang']))

            await db.commit()

        except aiosqlite.IntegrityError:
            print('Registration failed, user already exists.')


async def get_from_base(user_id: int) -> User:
    async with aiosqlite.connect('user_base.db') as db:
        return pickle.loads((await (await db.execute('SELECT user FROM UserBase WHERE id = ?',
                                                     (user_id,))).fetchone())[0])


async def update_user_obj(new_user_obj: User) -> None:
    async with aiosqlite.connect('user_base.db') as db:
        await db.execute('UPDATE UserBase SET user=? WHERE id=?',
                         (pickle.dumps(new_user_obj), new_user_obj.id))
        await db.commit()


async def get_lang(user_id: int) -> str:
    async with aiosqlite.connect('user_base.db') as db:
        # print(user_id)

        lang = (await (await db.execute('SELECT language FROM UserBase WHERE id = ?',
                                        (user_id,))).fetchone())[0]

        return lang


async def update_lang(user_id: int, lang: str):
    async with aiosqlite.connect('user_base.db') as db:
        await db.execute('UPDATE UserBase SET language=? WHERE id=?',
                         (lang, user_id))
        await db.commit()
