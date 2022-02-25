from itertools import groupby
import sqlite3
from flask import Flask, render_template, redirect, request, flash, url_for

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #name based access to columns
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NalaBear26!'

@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.title;').fetchall()
    # Get content of item and title of the list it belongs to
    # by joining both items and lists tables. Match list_id from items
    # table to id in lists table

    lists = {}
    print(todos)

    key_func = lambda t:t['title']

    for k, g in groupby(todos, key=key_func):
        lists[k] = list(g)


    conn.close()
    return render_template('index.html', lists = lists)

@app.route('/create/', methods=('GET','POST'))
def create():
    conn = get_db_connection()

    if request.method == 'POST':
        content = request.form['content']
        list_title = request.form['list']

        if not content:
            flash('Content is required')
            return redirect(url_for('index'))
        
        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);', (list_title,)).fetchone()['id'] # get list id from provided title
        conn.execute('INSERT INTO items (content, list_id) VALUES (?,?)', (content, list_id)) # insert new todo item into items table

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    lists = conn.execute('SELECT title FROM lists;').fetchall()

    conn.close()
    return render_template('create.html', lists=lists)