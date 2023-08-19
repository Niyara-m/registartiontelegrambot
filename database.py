import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, phone TEXT, location TEXT);')

def registration( id, name, phone, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, phone, location))
    connection.commit()

def check_registration(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False