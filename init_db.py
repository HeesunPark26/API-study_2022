import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute((
    "INSERT INTO user (username, bio, following, password)"
    f"VALUES ('elsie', 'hungry', 'false', '0000');"
    ))

connection.commit()
connection.close()
