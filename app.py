import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret'
DATABASE = 'giochi.db'


def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DATABASE)
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()


app.teardown_appcontext(close_db)


@app.route('/')
def index():
    conn = get_db()
    giochi = conn.execute('SELECT * FROM giochi ORDER BY id').fetchall()
    return render_template('index.html', giochi=giochi)


@app.route('/nuovo_gioco', methods=['GET', 'POST'])
def new_gioco():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        numero = request.form.get('numero_giocatori_massimo', '').strip()
        durata = request.form.get('durata_media', '').strip()
        categoria = request.form.get('categoria', '').strip()

        if not nome or not numero or not durata or not categoria:
            flash('Tutti i campi sono obbligatori!', 'error')
            return redirect(url_for('new_gioco'))

        try:
            numero_i = int(numero)
            durata_i = int(durata)
        except ValueError:
            flash('I campi "numero_giocatori_massimo" e "durata_media" devono essere numeri interi.', 'error')
            return redirect(url_for('new_gioco'))

        conn = get_db()
        conn.execute('INSERT INTO giochi (nome, numero_giocatori_massimo, durata_media, categoria) VALUES (?, ?, ?, ?)',
                     (nome, numero_i, durata_i, categoria))
        conn.commit()
        flash('Gioco aggiunto con successo!', 'success')
        return redirect(url_for('index'))

    return render_template('nuovo_gioco.html')


@app.route('/gioco/<int:gioco_id>/partite', methods=['GET', 'POST'])
def gioco_partite(gioco_id):
    conn = get_db()
    gioco = conn.execute('SELECT * FROM giochi WHERE id = ?', (gioco_id,)).fetchone()
    if gioco is None:
        flash('Gioco non trovato!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        data = request.form.get('data', '').strip()
        vincitore = request.form.get('vincitore', '').strip()
        punteggio = request.form.get('punteggio_vincitore', '').strip()

        if not data or not vincitore or not punteggio:
            flash('Tutti i campi della partita sono obbligatori!', 'error')
            return redirect(url_for('gioco_partite', gioco_id=gioco_id))

        try:
            punteggio_i = int(punteggio)
        except ValueError:
            flash('Il punteggio deve essere un numero intero.', 'error')
            return redirect(url_for('gioco_partite', gioco_id=gioco_id))

        conn.execute('INSERT INTO partite (gioco_id, data, vincitore, punteggio_vincitore) VALUES (?, ?, ?, ?)',
                     (gioco_id, data, vincitore, punteggio_i))
        conn.commit()
        flash('Partita aggiunta con successo!', 'success')
        return redirect(url_for('gioco_partite', gioco_id=gioco_id))

    partite = conn.execute('SELECT * FROM partite WHERE gioco_id = ? ORDER BY id', (gioco_id,)).fetchall()
    return render_template('partita.html', gioco=gioco, partite=partite)


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)