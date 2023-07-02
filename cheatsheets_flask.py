from flask import Flask, render_template, request
import random
import sqlite3

app = Flask(__name__)

def get_cheatsheets():
    res = ""
    conn = sqlite3.connect('static/cheatsheets.db') 
    cursor = conn.cursor()
    query = "SELECT angle, title, content FROM cheatsheets"  
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        angle = row[0]  # Extract angle
        title = row[1]  # Extract title
        content = row[2]  # Extract content
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
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            add_cheatsheet(title, content)
        
    cheatsheets_html = get_cheatsheets()
    return render_template("cheatsheets_index.html", content=cheatsheets_html)

app.run(host="0.0.0.0", port=8080)
