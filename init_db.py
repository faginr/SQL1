import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as file:
    connection.executescript(file.read())

cur = connection.cursor()

cur.execute("INSERT INTO lists (title) VALUES (?)", ('Work',))
cur.execute("INSERT INTO lists (title) VALUES (?)", ('Home',))
cur.execute("INSERT INTO lists (title) VALUES (?)", ('Study',))

cur.execute("INSERT INTO items (list_id, content) VALUES (?,?)", (1, 'Morning Meeting'))
cur.execute("INSERT INTO items (list_id, content) VALUES (?,?)", (2, 'Buy Fruit'))
cur.execute("INSERT INTO items (list_id, content) VALUES (?,?)", (2, 'Cook Dinner'))
cur.execute("INSERT INTO items (list_id, content) VALUES (?,?)", (3, 'Learn Flask'))
cur.execute("INSERT INTO items (list_id, content) VALUES (?,?)", (3, 'Learn SQLite'))

connection.commit()
connection.close()

