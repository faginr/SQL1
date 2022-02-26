from ast import keyword
from distutils.util import execute
from fileinput import close
from importlib.resources import contents
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
    todos = conn.execute('SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.title;').fetchall()
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

        new_list = request.form['new_list']
        # If a new list title is submitted, add to database
        if list_title == 'New List' and new_list:
            conn.execute('INSERT INTO lists (title) VALUES (?)', (new_list,))
            conn.commit()
            # Update list_title to refer to the newly added list
            list_title = new_list

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

@app.route('/<int:id>/do/', methods=('POST',))
def do(id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET done = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/<int:id>/undo/', methods=('POST',))
def undo(id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET done = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    
    # Use the id argument passed to the route to fetch the id of the to-do item you want
    # And the list it belongs to, value of done etc.
    todo = conn.execute('SELECT i.id, i.list_id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id WHERE l.id = ?', (id,)).fetchone()
    # get all todo lists from db
    lists = conn.execute('SELECT title FROM lists;').fetchall()


    if request.method == 'POST':
        content = request.form['content']
        list_title = request.form['list']

        if not content:
            flash('Content is required')
            return redirect(url_for('edit', id=id))

        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);', (list_title,)).fetchone()['id']

        # update content to what was submitted
        conn.execute('UPDATE items SET content = ?, list_id = ? WHERE id = ?', (content, list_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo, lists=lists)

# @app.route('/<int:id>/show/', methods=('GET', 'POST'))
# def show(id):
#     conn = get_db_connection()
#     todos = conn.execute('SELECT i.id, i.list_id, i.done, i.content, l.title, l.id FROM items i JOIN lists l ON i.list_id = l.id WHERE i.id = ?', (id,)).fetchone()    
#     lists = {}
#     print(todos)

#     key_func = lambda t:t['title']

#     for k, g in groupby(todos, key=key_func):
#         lists[k] = list(g)


#     conn.close()
#     return render_template('show.html', lists = lists)
    

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search/', methods=('GET', 'POST'))
def search(keyword="*"):
    if request.method == 'POST':
        keyword = request.form['keyword']
        conn = get_db_connection()
        contents = conn.execute('SELECT * FROM items WHERE content = ?', (keyword,)).fetchall()
        if keyword != "*":
            todos = conn.execute('SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id WHERE i.content=? ORDER BY l.title;', (keyword, )).fetchall()
        else:
            todos = conn.execute('SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.title;').fetchall()
        lists = {}

        key_func = lambda t:t['title']

        for k, g in groupby(todos, key=key_func):
            lists[k] = list(g)
        conn.commit()
        conn.close()
        return render_template('search.html', lists = lists)
    conn = get_db_connection()
    if keyword != "*":
        todos = conn.execute('SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id WHERE i.content=? ORDER BY l.title;', (keyword, )).fetchall()
    else:
        todos = conn.execute('SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.title;').fetchall()
    lists = {}

    key_func = lambda t:t['title']

    for k, g in groupby(todos, key=key_func):
        lists[k] = list(g)
    # contents = conn.execute('SELECT * FROM items').fetchall()
    conn.commit()
    conn.close()
    return render_template('search.html', lists=lists)

