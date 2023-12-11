
from .curs import st_c
from asyncio import run
import logging

def _get_db() -> None:
        return st_c()


async def get_data_from_users(user_id: int):
    cur, connection = _get_db()
    one_result = cur.execute(f'SELECT * FROM Users WHERE user_id=({str(user_id)});''').fetchone()
    connection.commit()
    connection.close()
    return one_result

async def add_items_db(args):
    cur, connection = _get_db()
    v = ", ".join(args[:-1])
    logging.info(v)
    cur.execute(f"INSERT INTO Users(user_id, user_h, user_w, user_a, sex) VALUES ({v}, '{args[-1]}')")
    connection.commit()
    return "succes"

async def update_items_db(user_id: int, uh, uw, ua, us):
    cur, connection = _get_db()
    cur.execute(f"UPDATE Users SET user_h = {uh}, user_w = {uw}, user_a = {ua}, sex = '{us}' WHERE user_id=({str(user_id)});")
    connection.commit()
    return "succes"

# # print(run(add_items_db(['1', "2", '3', '4'])))
# print(run(get_data_from_users(user_id=1)))








# # print(get_data_from_p(inline_id="1", args=["post_id", "inline_id", "post_text1", "post_text2", "post_text3", "post_text4"]), sep="\n")

# # print(add_item(args=['aaaa ', 'текст2 ', 'текст3 ', 'текст4'])) 

