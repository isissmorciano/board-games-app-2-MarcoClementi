from flask import Flask, render_template, request, redirect, url_for, flash, g, Blueprint
import sqlite3

app = Flask(__name__)
bp = Blueprint('main', __name__)
DATABASE = 'schema.sql'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@bp.route('/')
def index():
    conn = get_db()
    giochi = conn.execute('SELECT * FROM giochi').fetchall()
    conn.close()
    return render_template('index.html', giochi=giochi)


@bp.route ("/nuovo_gioco, methods=['GET', 'POST']")
def nuovo_gioco():
    if request.method == 'POST':
        nome = request.form['nome']
        descrizione = request.form['descrizione']
        conn = get_db()
        conn.execute('INSERT INTO giochi (nome, descrizione) VALUES (?, ?)', (nome, descrizione))
        conn.commit()
        conn.close()
        flash('Gioco aggiunto con successo!')
        return redirect(url_for('index'))

@bp.route('/gioco/<int:id>')
def gioco(id):
    conn = get_db()
    gioco = conn.execute('SELECT * FROM giochi WHERE id = ?', (id,)).fetchone()
    conn.close()
    if gioco is None:
        flash('Gioco non trovato!')
        return redirect(url_for('index'))
    return render_template('gioco.html', gioco=gioco)
app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True)

