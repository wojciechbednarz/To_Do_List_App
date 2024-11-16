import sqlite3
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("todo_list_app.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
            )
            """)
        conn.commit()


@app.route("/add", methods=["POST"])
def add_task():
    if request.method != "POST":
        return redirect(url_for("index"))
    data = request.form.get("data")
    if not data:
        return "Error: Task description cannot be empty", 400
    with get_db_connection() as conn:
        conn.execute("""
        INSERT INTO tasks (items, completed)
        VALUES (?, ?)""", (data, False))
        conn.commit()
    return redirect(url_for("index"))


def add_task_from_gui(item):
    try:
        with get_db_connection() as conn:
            conn.execute("""
            INSERT INTO tasks (items, completed)
            VALUES (?, ?)""", (item, False))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error {e}")


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    with get_db_connection() as conn:
        conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    with get_db_connection() as conn:
        conn.execute("DELETE from tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))


@app.route("/")
def index():
    with get_db_connection() as conn:
        tasks = conn.execute("""
                SELECT id, items, completed FROM tasks
                """).fetchall()
    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
