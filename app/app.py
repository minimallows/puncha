from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Database initialization
def init_db():
    with sqlite3.connect("puns.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS puns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pun TEXT NOT NULL
            )
        """)

# Function to load all puns
def load_puns():
    with sqlite3.connect("puns.db") as conn:
        return [row[0] for row in conn.execute("SELECT pun FROM puns")]

# Function to save a pun
def save_pun(pun):
    with sqlite3.connect("puns.db") as conn:
        conn.execute("INSERT INTO puns (pun) VALUES (?)", (pun,))

# Initialize database
init_db()

@app.route('/')
def homepage():
    PUNS = load_puns()  # Fetch all puns from the database
    pun = random.choice(PUNS) if PUNS else "No puns available yet! Submit one below!"
    return render_template('index.html', pun=pun)

@app.route('/submit', methods=['GET', 'POST'])
def submit_pun():
    if request.method == 'POST':
        new_pun = request.form.get('pun')
        if new_pun:
            save_pun(new_pun)  # Save to the database
        return redirect(url_for('homepage'))
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
