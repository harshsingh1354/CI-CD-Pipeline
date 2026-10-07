import hashlib
import os
import pickle
import sqlite3
import subprocess

from flask import Flask, request, render_template_string

app = Flask(__name__)

API_KEY = "9f8e7d6c5b4a39281706f5e4d3c2b1a09f8e7d6c"
DB_PASSWORD = "SuperSecret@12345"


def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)")
    return conn


@app.route("/")
def home():
    return "Vulnerable demo app"


@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    rows = get_db().execute(query).fetchall()
    return str(rows)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output


@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template_string("<h1>Hello " + name + "</h1>")


@app.route("/calc")
def calc():
    expression = request.args.get("expr", "1+1")
    return str(eval(expression))


@app.route("/file")
def read_file():
    filename = request.args.get("name", "readme.txt")
    with open(os.path.join("files", filename)) as f:
        return f.read()


@app.route("/load", methods=["POST"])
def load():
    data = pickle.loads(request.data)
    return str(data)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    password = hashlib.md5(request.form.get("password", "").encode()).hexdigest()
    conn = get_db()
    conn.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    return "registered"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
