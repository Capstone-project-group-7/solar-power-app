from flask_cors import CORS
from numpy import array
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
app = Flask(__name__)
# enable cors
CORS(app)
# load the models from disk

# Default home page
@app.route('/')
def home():
    return render_template('index.html')
def _init_(self):
    con=sqlite3.connect('user.db')
    c=con.cursor
    c.execute("Create table user(name text, password text)")
    con.commit()
# Radiation model api endpoint http://127.0.0.1:8000/api/model/radiation

# login end point
@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html')
# route when log out clicked - rediracts to home page

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('index.html'))

# route when sign up clicked - rediracts to register page
@app.route('/register', methods =['GET', 'POST'])
def register():
    return render_template('register.html')

# route when log in is successful - navigates to main application page
@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')
# route when history is clicked - navigates to history page

@app.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('history.html')


if __name__ == "__main__":
    app.run(debug=True)