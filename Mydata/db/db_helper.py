
from .curs import st_c
from asyncio import run
import logging

def _get_db() -> None:
        return st_c()


async def get_data_from_users(user_id: int):
    cur, connection = _get_db()[0]
    one_result = cur.execute(f'SELECT * FROM Users WHERE user_id=({str(user_id)});''').fetchone()
    connection.commit()
    connection.close()
    return one_result

async def add_items_db(args, db):
    if db == 1:
        cur, connection = _get_db()[0]
        v = ", ".join(args[:-2])
        logging.info(v)
        cur.execute(f"INSERT INTO Users(user_id, user_h, user_w, user_a, shnap, sex) VALUES ({v}, '{args[-2]}', '{args[-1]}')")
        connection.commit()
        connection.close()
        return "succes"
    elif db == 2:
        cur, connection = _get_db()[1]
        v = ", ".join(args)
        from datetime import datetime
        logging.info(v)
        print(v)
        cur.execute(f"INSERT INTO Users_nastr(user_id, moodness, day) VALUES ({args[0]}, '{args[1]}', '{datetime.now().strftime('%d.%m.%y')}')")
        connection.commit()
        connection.close()
        return "succes"
    else:
        raise 'Не та база'
    
async def update_items_db(user_id: int, uh, uw, ua, us):
    cur, connection = _get_db()[0]
    cur.execute(f"UPDATE Users SET user_h = {uh}, user_w = {uw}, user_a = {ua}, sex = '{us}' WHERE user_id=({str(user_id)});")
    connection.commit()
    return "succes"


async def update_shnap(user_id: int, sh):
    cur, connection = _get_db()[0]
    cur.execute(f"UPDATE Users SET shnap = '{sh}' WHERE user_id=({str(user_id)});")
    connection.commit()
    connection.close()
    return "succes"


async def get_happy_data(user_id: int):
    cur, connection = _get_db()[1]
    results = cur.execute(f'SELECT * FROM Users_nastr WHERE user_id=({str(user_id)});''').fetchall()
    connection.commit()
    connection.close()
    return results





# print(run(add_items_db(['1231', '2'], 2)))









# # print(get_data_from_p(inline_id="1", args=["post_id", "inline_id", "post_text1", "post_text2", "post_text3", "post_text4"]), sep="\n")

# # print(add_item(args=['aaaa ', 'текст2 ', 'текст3 ', 'текст4'])) 

