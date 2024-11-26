from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request
import random
import sqlite3

app = Flask(__name__)

def get_snippets(searchQuery):
    res = ""
    conn = sqlite3.connect('static/snippets.db') 
    cursor = conn.cursor()
    query = "SELECT title, content FROM snippets"
    values = ()
    if searchQuery:
        query += " WHERE title LIKE ? OR content LIKE ?"
        values = ('%' + searchQuery + '%', '%' + searchQuery + '%')
    query += " LIMIT 20"
    cursor.execute(query, values)
    rows = cursor.fetchall()
    for row in rows:
        title, content = row[0], row[1]
        res += f"\r\n  <gp-postit-note title=\"{title}\" class=\"item\">\r\n    {content}\r\n  </gp-postit-note>"
    conn.close()
    return res

def add_snippet(title, content):
    conn = sqlite3.connect('static/snippets.db') 
    cursor = conn.cursor()

    # Check if the snippet already exists
    query = "SELECT COUNT(*) FROM snippets WHERE title = ? AND content = ?"
    values = (title, content)
    cursor.execute(query, values)
    count = cursor.fetchone()[0]

    if count > 0:
        return

    query = "INSERT INTO snippets (title, content) VALUES (?, ?)"
    values = (title, content)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def add_user(email, password):
    hashed_password = pbkdf2_sha256.hash(password) # hash password
    conn = sqlite3.connect('static/snippets.db') 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    # Add user with hashed password to the database
    add_user(username, password)
    return "User registered successfully."

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        hashed_password = result[0]
        if pbkdf2_sha256.verify(password, hashed_password):
            return "Login successful"
    return "Invalid credentials"

@app.route("/", methods=['GET', 'POST'])
def index():
    search = ""
    if request.method == 'GET':
        search = request.args.get('search')
        if search is None:
            search = ''
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            add_snippet(title, content)
        
    snippets_html = get_snippets(search)
    print(search)
    return render_template("snippets_index.html", content=snippets_html, search = search)

app.run(host="0.0.0.0", port=8080)
