from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions


# -----------------------------
# Helpers auth
# -----------------------------
def est_authentifie():
    return session.get('authentifie')

def est_authentifie_user():
    return session.get('authentifie_user')


# -----------------------------
# Routes EXISTANTES (ta 1ère app)
# -----------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)',
        (1002938, nom, prenom, "ICI")
    )
    conn.commit()
    conn.close()
    return redirect('/consultation/')

@app.route('/authentification_user', methods=['GET', 'POST'])
def authentification_user():
    if request.method == 'POST':
        if request.form['username'] == 'user' and request.form['password'] == '12345':
            session['authentifie_user'] = True
            return redirect(url_for('fiche_nom'))
        else:
            return render_template('formulaire_authentification_user.html', error=True)

    return render_template('formulaire_authentification_user.html', error=False)

@app.route('/fiche_nom/', methods=['GET', 'POST'])
def fiche_nom():
    if not est_authentifie_user():
        return redirect(url_for('authentification_user'))

    data = []
    if request.method == 'POST':
        nom = request.form['nom']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE nom LIKE ?', ('%' + nom + '%',))
        data = cursor.fetchall()
        conn.close()

    return render_template('fiche_nom.html', data=data)

@app.route('/livres')
def ReadBDDForBooks():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data_books.html', data=data)

@app.route('/recherche_livre/', methods=['GET', 'POST'])
def search_results():
    data = []
    if request.method == 'POST':
        titre = request.form['titre']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',))
        data = cursor.fetchall()
        conn.close()

    return render_template('search_books.html', data=data)


# -----------------------------
# TODO APP (dans la même app Flask)
# -----------------------------
DB_NAME_TODO = "database_todo.db"

def get_todo_db():
    conn = sqlite3.connect(DB_NAME_TODO)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/todo/")
def todo_home():
    return render_template("home_todo.html")

@app.get("/todo/tasks")
def todo_tasks():
    filter_ = request.args.get("filter", "all")
    db = get_todo_db()

    if filter_ == "done":
        rows = db.execute("SELECT * FROM tasks WHERE is_done=1 ORDER BY created_at DESC").fetchall()
    elif filter_ == "active":
        rows = db.execute("SELECT * FROM tasks WHERE is_done=0 ORDER BY created_at DESC").fetchall()
    else:
        rows = db.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()

    db.close()
    return render_template("tasks.html", tasks=rows, filter=filter_)

@app.get("/todo/tasks/new")
def todo_new_task():
    return render_template("add.html")

@app.post("/todo/tasks")
def todo_add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "").strip() or None

    if not title:
        return redirect(url_for("todo_new_task"))

    db = get_todo_db()
    db.execute(
        "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, 0)",
        (title, description, due_date),
    )
    db.commit()
    db.close()

    return redirect(url_for("todo_tasks"))

@app.post("/todo/tasks/<int:task_id>/toggle")
def todo_toggle_task(task_id):
    filter_ = request.args.get("filter", "all")
    db = get_todo_db()
    db.execute(
        "UPDATE tasks SET is_done = CASE is_done WHEN 0 THEN 1 ELSE 0 END WHERE id=?",
        (task_id,),
    )
    db.commit()
    db.close()
    return redirect(url_for("todo_tasks", filter=filter_))

@app.post("/todo/tasks/<int:task_id>/delete")
def todo_delete_task(task_id):
    filter_ = request.args.get("filter", "all")
    db = get_todo_db()
    db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    db.commit()
    db.close()
    return redirect(url_for("todo_tasks", filter=filter_))


if __name__ == "__main__":
    app.run(debug=True)
