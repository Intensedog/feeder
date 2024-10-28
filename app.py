#!/home/pi/venv/feeder/bin/python
from __future__ import with_statement
import sys
import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, Response, session, url_for, abort
from flask_cors import CORS
from gpiozero.pins.pigpio import PiGPIOFactory
from markupsafe import Markup
import subprocess
import configparser
import datetime
from gpiozero import AngularServo
from time import sleep
from werkzeug.security import check_password_hash, generate_password_hash
from stat import S_ISREG, ST_CTIME, ST_MODE

sys.path.extend(['/var/www/feeder/feeder/logs'])

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages
CORS(app)

# Define database path globally
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'feeder.db')

# Initialize SQLite database
def init_db():
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
        print("Database initialized at:", DATABASE)
    except sqlite3.Error as e:
        print("Database initialization error:", e)

# Database connection helper
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password)
                    VALUES (?, ?)
                ''', (username, hashed_password))
                conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another one.")
            return render_template('register.html')

    return render_template('register.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
                record = cursor.fetchone()

            if record and check_password_hash(record[0], password):
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password.")
                return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash("Database error occurred. Please try again.")
            print("Database error:", e)
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        servo_pin = 18
        servo = AngularServo(servo_pin, min_angle=-90, max_angle=90)

        def open_servo():
            print("Opening servo...")
            servo.angle = 90

        def close_servo():
            print("Closing servo...")
            servo.angle = -90

        open_servo()
        sleep(1)
        close_servo()
        sleep(1)

    return render_template('home.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=False, 
            host='0.0.0.0',
            threaded=True, 
            port=5000)