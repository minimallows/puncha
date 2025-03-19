from flask import Flask, render_template, jsonify
import sqlite3
import random
import os

# Ensure Flask looks for templates in the right folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder="../static")

# Function to fetch a pun from the database
def load_puns():
    conn = sqlite3.connect("../puns.db")  # Adjust path if needed
    cursor = conn.cursor()
    cursor.execute("SELECT pun_text FROM puns")
    puns = cursor.fetchall()
    conn.close()
    return [pun[0] for pun in puns]

# Route to serve the HTML page
@app.route('/')
def homepage():
    return render_template('index.html')

# API route to fetch a random pun
@app.route('/api/pun')
def get_random_pun():
    PUNS = load_puns()
    pun = random.choice(PUNS) if PUNS else "No puns available!"
    return jsonify({"pun": pun})

if __name__ == '__main__':
    app.run(debug=True)
