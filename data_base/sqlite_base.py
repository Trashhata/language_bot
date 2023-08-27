import aiosqlite
import pickle
from data_base.users import User


async def initiate_user_base():
    con = await aiosqlite.connect('user_base.db')
    await con.execute('create table if not exists UserBase (id int, user text, language text, UNIQUE(id, user))')

    await con.commit()


async def write_into_base(user_info: dict):
    con = await aiosqlite.connect('user_base.db')

    try:
        await con.execute(f"""
            INSERT INTO UserBase (id, user, language) 
            VALUES (?, ?, ?)
        """, (user_info['id'], pickle.dumps(User(user_info)), user_info['lang']))

        await con.commit()

    except aiosqlite.IntegrityError:
        print('Registration failed, user already exists.')


async def get_from_base(user_id: int) -> User:
    con = await aiosqlite.connect('user_base.db')

    return pickle.loads((await (await con.execute('SELECT user FROM UserBase WHERE id = ?',
                                                  (user_id,))).fetchone())[0])


async def update_user_obj(new_user_obj: User) -> None:
    con = await aiosqlite.connect('user_base.db')

    await con.execute('UPDATE UserBase SET user=? WHERE id=?',
                      (pickle.dumps(new_user_obj), new_user_obj.id))
    await con.commit()


async def get_lang(user_id: int) -> str:
    con = await aiosqlite.connect('user_base.db')

    lang = (await (await con.execute('SELECT language FROM UserBase WHERE id = ?',
                                     (user_id,))).fetchone())[0]

    return lang
