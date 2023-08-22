import sqlite3
import pickle
from data_base.users import User


async def initiate_user_base():
    con = sqlite3.connect('user_base.db')
    cur = con.cursor()

    cur.execute('create table if not exists UserBase (id int, user text, UNIQUE(id, user))')

    con.commit()


async def write_into_base(user_info: dict):
    con = sqlite3.connect('user_base.db')
    cur = con.cursor()

    try:
        cur.execute(f"""
            INSERT INTO UserBase (id, user) 
            VALUES (?, ?)
        """, (user_info['id'], pickle.dumps(User(user_info))))

        con.commit()

    except sqlite3.IntegrityError:
        print('Registration failed, user already exists.')


async def get_from_base(user_id: int) -> User:
    con = sqlite3.connect('user_base.db')
    cur = con.cursor()

    return pickle.loads(cur.execute('SELECT user FROM UserBase WHERE id = ?',
                                    (user_id,)).fetchone()[0])


async def update_user_obj(new_user_obj: User) -> None:
    con = sqlite3.connect('user_base.db')
    cur = con.cursor()

    cur.execute('UPDATE UserBase SET user=? WHERE id=?',
                (pickle.dumps(new_user_obj), new_user_obj.id))
    con.commit()
