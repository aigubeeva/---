import sqlite3

def st_c():
    connection1 = sqlite3.connect('Mydata\db\\users.db')
    cur1 = connection1.cursor()
    
    cur1.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        user_h INTEGER,
        user_w INTEGER,
        user_a INTEGER,
        sex TEXT,
        shnap TEXT
        )
    ''')


    connection2 = sqlite3.connect('Mydata\db\\users_nastr.db')
    cur2 = connection2.cursor()
    
    cur2.execute('''
        CREATE TABLE IF NOT EXISTS Users_nastr (
        user_id INTEGER,
        moodness INTEGER,
        day TEXT
        )
    ''')
    return (cur1, connection1), (cur2, connection2)


# print(st_c())