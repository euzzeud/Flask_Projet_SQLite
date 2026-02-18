import sqlite3

connection = sqlite3.connect("database_todo.db")

with open("schema_todo.sql", "r", encoding="utf-8") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, ?)",
    ("Faire les courses", "Lait, œufs, pâtes, fruits", "2026-02-20", 0),
)
cur.execute(
    "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, ?)",
    ("Réviser Flask", "Routes, templates, SQLite", "2026-02-22", 0),
)
cur.execute(
    "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, ?)",
    ("Envoyer le devoir", "Vérifier le README + lien alwaysdata", "2026-02-25", 0),
)
cur.execute(
    "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, ?)",
    ("Faire du sport", "30 minutes minimum", None, 0),
)
cur.execute(
    "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, ?)",
    ("Ranger le bureau", "Trier papiers + câbles", "2026-02-19", 1),
)

connection.commit()
connection.close()