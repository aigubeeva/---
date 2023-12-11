import sqlite3

def st_c():
    connection = sqlite3.connect('data\db\\users.db')
    cur = connection.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        user_h INTEGER,
        user_w INTEGER,
        user_a INTEGER,
        sex TEXT
        )
    ''')
    return (cur, connection)

