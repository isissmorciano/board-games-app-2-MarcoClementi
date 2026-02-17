import os
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret'
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        conn = get_db()
        with app.open_resource('schema.sql') as f:
            conn.executescript(f.read().decode('utf8'))
        conn.close()
    app.run(debug=True)






















































































