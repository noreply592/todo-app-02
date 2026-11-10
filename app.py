import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "todo.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )"""
        )


@app.route("/")
def index():
    status = request.args.get("filter", "all")
    sql = "SELECT * FROM todos"
    if status == "active":
        sql += " WHERE done = 0"
    elif status == "done":
        sql += " WHERE done = 1"
    sql += " ORDER BY done, id DESC"
    todos = get_db().execute(sql).fetchall()
    remaining = get_db().execute("SELECT COUNT(*) FROM todos WHERE done = 0").fetchone()[0]
    return render_template("index.html", todos=todos, status=status, remaining=remaining)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        db = get_db()
        db.execute("INSERT INTO todos (title) VALUES (?)", (title,))
        db.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    db = get_db()
    db.execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
    db.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit(todo_id):
    title = request.form.get("title", "").strip()
    if title:
        db = get_db()
        db.execute("UPDATE todos SET title = ? WHERE id = ?", (title, todo_id))
        db.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/clear", methods=["POST"])
def clear_done():
    db = get_db()
    db.execute("DELETE FROM todos WHERE done = 1")
    db.commit()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
