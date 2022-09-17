from asyncio.windows_events import NULL
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flaskext.mysql import MySQL
from random import randint
import pymysql
import re
import random
import string
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'Thinkfinity Labs'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_pASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'user-cred'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#this will be the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM credentials WHERE username = %s OR email = %s AND password = %s', (username, username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            session['email'] = account['email']
            
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            return redirect(url_for('login'))

    return render_template('login.html', msg=msg)

# this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        

    # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM credentials WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!' 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO credentials VALUES (%s, %s, %s)',
                            (username, email, password))
            conn.commit()
            return render_template('login.html', msg=msg)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
            
         # User is loggedin show them the home page
        return render_template('index.html',username=session.get('username'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/')
def home2():
    # Check if user is loggedin
    if 'loggedin' in session:
            
         # User is loggedin show them the home page
        return render_template('index.html',username=session.get('username'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
