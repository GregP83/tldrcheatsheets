from flask import Flask, render_template, request
import random
import sqlite3

app = Flask(__name__)

def get_cheatsheets(searchQuery):
    res = ""
    conn = sqlite3.connect('static/cheatsheets.db') 
    cursor = conn.cursor()
    query = "SELECT angle, title, content FROM cheatsheets"
    values = ()
    if searchQuery:
        query += " WHERE title LIKE ? OR content LIKE ?"
        values = ('%' + searchQuery + '%', '%' + searchQuery + '%')
    cursor.execute(query, values)
    rows = cursor.fetchall()
    for row in rows:
        angle, title, content = row[0], row[1], row[2]
        res += f"\r\n  <gp-postit-note degrees=\"{str(angle)}\" title=\"{title}\">\r\n    {content}\r\n  </gp-postit-note>"
    conn.close()
    return res

def add_cheatsheet(title, content):
    conn = sqlite3.connect('static/cheatsheets.db') 
    cursor = conn.cursor()
    random_angle = random.randint(-3, 3)
    query = "INSERT INTO cheatsheets (angle, title, content) VALUES (?, ?, ?)"
    values = (random_angle, title, content)
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
            add_cheatsheet(title, content)
        
    cheatsheets_html = get_cheatsheets(search)
    return render_template("cheatsheets_index.html", content=cheatsheets_html)

app.run(host="0.0.0.0", port=8080)