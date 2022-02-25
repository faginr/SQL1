from itertools import groupby
from app import get_db_connection

conn = get_db_connection()
todos = conn.execute('SELECT i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY title;').fetchall()

lists = {}

# groupby will go through each item in the todos variable
# which is everything returned from the sql select
# k is list titles
# g is the group that contains the to-do items of each list title.
for k,g in groupby(todos, key=lambda t: t['title']):
    lists[k] = list(g)

for list_, items in lists.items():
    print(list_)
    for item in items:
        print('   ', item['content'])