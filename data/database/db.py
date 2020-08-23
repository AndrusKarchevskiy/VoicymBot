from datetime import datetime
from typing import Union

import aiosqlite as lite

db_path = 'data/database/data.db'


async def add_new_user(user_id: int, user_name: str):
    async with lite.connect(db_path) as con:
        cur = await con.cursor()
        await cur.execute("SELECT user_id FROM tbl_users WHERE user_id = ?", (user_id,))

        if not (user_id,) in await cur.fetchall():
            today = datetime.now()
            today = today.strftime("%d.%m.%Y")
            await cur.execute("INSERT INTO tbl_users(user_id, user_name, sent_audio_files, sent_texts, time_reg) "
                              "VALUES(?, ?, ?, ?, ?)", (user_id, user_name, 0, 0, str(today)))
            await con.commit()


async def get_user_param(user_id: int, column: str) -> Union[int, str]:
    async with lite.connect(db_path) as con:
        cur = await con.cursor()
        await cur.execute(f"SELECT {column} FROM tbl_users WHERE user_id = ?", (user_id,))
        param = await cur.fetchall()
        return param[0][0]


async def change_user_param(user_id: int, column: str, param: Union[int, str]):
    async with lite.connect(db_path) as con:
        cur = await con.cursor()
        await cur.execute(f"UPDATE tbl_users SET {column} = ? WHERE user_id = ?", (param, user_id,))
        await con.commit()


async def update_user_param(user_id: int, column: str):
    async with lite.connect(db_path) as con:
        cur = await con.cursor()
        await cur.execute(f"SELECT {column} FROM tbl_users WHERE user_id = ?", (user_id,))
        param_from_db = await cur.fetchall()
        updated_param = param_from_db[0][0] + 1
        await cur.execute(f"UPDATE tbl_users SET {column} = ? WHERE user_id = ?", (updated_param, user_id,))
        await con.commit()


async def downgrade_user_param(user_id: int, column: str):
    async with lite.connect(db_path) as con:
        cur = await con.cursor()
        await cur.execute(f"SELECT {column} FROM tbl_users WHERE user_id = ?", (user_id,))
        param_from_db = await cur.fetchall()
        downgraded_param = param_from_db[0][0] - 1
        await cur.execute(f"UPDATE tbl_users SET {column} = ? WHERE user_id = ?", (downgraded_param, user_id,))
        await con.commit()
