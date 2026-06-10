from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

app.secret_key = "your_secret_key_here"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "user_id" not in session:
        return "You must be logged in to upload files"

    file = request.files["file"]

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO documents (filename, filepath, user_id)
            VALUES (?, ?, ?)
        """, (file.filename, filepath, session["user_id"]))

        conn.commit()
        conn.close()

        return "File uploaded successfully!"

    return "No file selected"

from flask import render_template

@app.route("/files")
def files():
    if "user_id" not in session:
        return "Please login first"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM documents WHERE user_id=?
    """, (session["user_id"],))

    data = cursor.fetchall()
    conn.close()

    return render_template("files.html", files=data)

import sqlite3

from flask import session, redirect, url_for, request
import sqlite3

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, password))

        conn.commit()
        conn.close()

        return "User registered successfully!"

    return '''
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" placeholder="Password" type="password">
        <button type="submit">Register</button>
    </form>
    '''


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return "Login successful!"
        else:
            return "Invalid credentials"

    return '''
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)