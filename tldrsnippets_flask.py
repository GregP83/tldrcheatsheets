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
    query += " LIMIT 100"
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

@app.route("/", methods=['GET', 'POST'])
def index():
    search = None
    if request.method == 'GET':
        search = request.args.get('search')
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            add_snippet(title, content)
        
    snippets_html = get_snippets(search)
    return render_template("snippets_index.html", content=snippets_html, search = search)

app.run(host="0.0.0.0", port=8080)