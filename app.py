from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Nødvendig for å bruke sessions

# Last inn variabler fra .env-filen
load_dotenv('hidden.env')

# Funksjon for å koble til MySQL-databasen
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# her skal sjekke passord funksjonen være


# Hjemmesiden
@app.route('/')
def index():
    return render_template('index.html')

# Logg inn-side
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Sjekk om brukeren finnes og passordet stemmer
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = %s', (username,))
        user = c.fetchone()
        conn.close()

        # Sjekk passordet mot det hashede passordet i databasen
        if user and check_password_hash(user[0], password):
            session['username'] = username  # Lagre brukeren i session
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'  # Feilmelding hvis feil info

    return render_template('login.html')  # Viser login-skjema

# Registreringsside
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 
        
        # Lag hash av passordet før det lagres
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        c = conn.cursor()
        try:
            # Legg til ny bruker i databasen
            c.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
        except mysql.connector.IntegrityError:
            return 'Username already exists'  # Hvis brukernavn allerede finnes
        finally:
            conn.close()

        return redirect(url_for('login'))  # Gå til login etter registrering

    return render_template('register.html')  # Viser registreringsskjema

# Logg ut brukeren
@app.route('/logout')
def logout():
    session.pop('username', None)  # Fjern brukeren fra session
    return redirect(url_for('index'))

# Viser ledertavlen
@app.route('/leaderboard')
def leaderboard():
    conn = get_db_connection()
    c = conn.cursor()

    # Hent brukernavn og poeng sortert etter høyeste poengsum
    c.execute('SELECT username, score FROM leaderboard ORDER BY score DESC')
    leaderboard = c.fetchall()
    conn.close()

    return render_template('leaderboard.html', leaderboard=leaderboard)

# Tar imot og lagrer poeng fra klienten
@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 403

    data = request.get_json()
    try:
        # Forsøk å hente og validere poeng
        score = int(data.get('score', 0))
        if score < 0 or score > 999999:
            raise ValueError  # Ugyldig poeng
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid score'}), 400

    # Lagre poeng i databasen
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO leaderboard (username, score) VALUES (%s, %s)', (session['username'], score))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

# Chat-funksjon
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            message = request.form['message']

            # Lagre ny melding i databasen
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO chat (username, message) VALUES (%s, %s)', (username, message))
            conn.commit()
            conn.close()

    # Hent chat-meldinger, nyeste først
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, message, timestamp FROM chat ORDER BY timestamp DESC')
    chat_messages = c.fetchall()
    conn.close()

    return render_template('chat.html', chat_messages=chat_messages)

# Start Flask-serveren
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0") 