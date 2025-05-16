from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host='10.2.2.229',
        port=3306,
        user='user',
        password='brukerpassord',
        database='gyro_clicker'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = %s', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[0], password):
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
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
        except mysql.connector.IntegrityError:
            return 'Username already exists'
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, score FROM leaderboard ORDER BY score DESC')
    leaderboard = c.fetchall()
    conn.close()
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 403

    data = request.get_json()
    try:
        score = int(data.get('score', 0))
        if score < 0 or score > 999999:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid score'}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO leaderboard (username, score) VALUES (%s, %s)', (session['username'], score))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            message = request.form['message']
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO chat (username, message) VALUES (%s, %s)', (username, message))
            conn.commit()
            conn.close()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, message, timestamp FROM chat ORDER BY timestamp DESC')
    chat_messages = c.fetchall()
    conn.close()
    return render_template('chat.html', chat_messages=chat_messages)

if __name__ == '__main__':
    app.run(debug=True)
