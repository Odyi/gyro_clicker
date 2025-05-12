from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('gyro_clicker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    score INTEGER NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('gyro_clicker.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[0], password):  # Verify hashed password
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Hash the password
        conn = sqlite3.connect('gyro_clicker.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('gyro_clicker.db')
    c = conn.cursor()
    c.execute('SELECT username, score FROM leaderboard ORDER BY score DESC')
    leaderboard = c.fetchall()
    conn.close()
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'username' in session:
        username = session['username']
        score = request.form['score']
        conn = sqlite3.connect('gyro_clicker.db')
        c = conn.cursor()
        c.execute('INSERT INTO leaderboard (username, score) VALUES (?, ?)', (username, score))
        conn.commit()
        conn.close()
    return redirect(url_for('leaderboard'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            message = request.form['message']
            conn = sqlite3.connect('gyro_clicker.db')
            c = conn.cursor()
            c.execute('INSERT INTO chat (username, message) VALUES (?, ?)', (username, message))
            conn.commit()
            conn.close()
    conn = sqlite3.connect('gyro_clicker.db')
    c = conn.cursor()
    c.execute('SELECT username, message, timestamp FROM chat ORDER BY timestamp DESC')
    chat_messages = c.fetchall()
    conn.close()
    return render_template('chat.html', chat_messages=chat_messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

    #SQL CODE without mariadb
    