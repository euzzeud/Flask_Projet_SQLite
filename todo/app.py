from flask import Flask
from routes import bp

app = Flask(__name__)


ef get_db():
    conn = sqlite3.connect("database_todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@bp.get("/todo/")
def index():
    return redirect(url_for("todo.tasks"))

@bp.get("/todo/tasks")
def tasks():
    filter_ = request.args.get("filter", "all")
    db = get_db()

    if filter_ == "done":
        rows = db.execute("SELECT * FROM tasks WHERE is_done=1 ORDER BY created_at DESC").fetchall()
    elif filter_ == "active":
        rows = db.execute("SELECT * FROM tasks WHERE is_done=0 ORDER BY created_at DESC").fetchall()
    else:
        rows = db.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()

    db.close()
    return render_template("tasks.html", tasks=rows, filter=filter_)

@bp.get("/todo/tasks/new")
def new_task():
    return render_template("add.html")

@bp.post("/todo/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "").strip() or None

    if not title:
        return redirect(url_for("todo.new_task"))

    db = get_db()
    db.execute(
        "INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, 0)",
        (title, description, due_date),
    )
    db.commit()
    db.close()
    return redirect(url_for("todo.tasks"))

@bp.post("/todo/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    db = get_db()
    db.execute(
        "UPDATE tasks SET is_done = CASE is_done WHEN 0 THEN 1 ELSE 0 END WHERE id=?",
        (task_id,),
    )
    db.commit()
    db.close()
    return redirect(url_for("todo.tasks", filter=request.args.get("filter", "all")))

@bp.post("/todo/tasks/<int:task_id>/delete")
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    db.commit()
    db.close()
    return redirect(url_for("todo.tasks", filter=request.args.get("filter", "all")))


if __name__ == "__main__":
    app.run(debug=True)
