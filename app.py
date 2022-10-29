import sqlite3
from flask_cors import CORS
from numpy import array
import tensorflow as tf
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template,flash, redirect, url_for, session
​
​
app = Flask(__name__)
app.secret_key="1234"
​
con=sqlite3.connect("database.db")
con.execute("create table if not exists customer(pid integer primary key,name text,mail text,password integer unique,address text)")
con.close()
​
# enable cors
CORS(app)
​
# load the models from disk
#filename2 = r'model2.h5'
​
​
# Loading a saved model
#from numpy import loadtxt
#from tensorflow.keras.models import load_model
​
#model = load_model(filename2)
​
# Default home page
@app.route('/')
def home():
    return render_template('index.html')
​
# Radiation model api endpoint http://127.0.0.1:8000/api/model/radiation
@app.route('/predict',methods=['POST'])
def predict():
    first_interval = request.form.get('first_interval')
    second_interval = request.form.get('second_interval')
    third_interval = request.form.get('third_interval')
    capacity_of_one_panel = request.form.get('capacity_of_one_panel')
    number_of_solar_panels = request.form.get('number_of_solar_panels')
    area_of_panel = request.form.get('area_of_panel')
    actual_solar_radiation = array(
        [float(first_interval), float(second_interval), float(third_interval)])
    actual_solar_radiation = actual_solar_radiation.reshape((1, 3, 1))
    capacity_of_one_panel = float(capacity_of_one_panel)
    number_of_solar_panels = float(number_of_solar_panels)
    area_of_panel = float(area_of_panel)
    yield_of_one_panel = (capacity_of_one_panel)/(area_of_panel * 10)
    predictions = model.predict(actual_solar_radiation)*0.75*number_of_solar_panels*area_of_panel*yield_of_one_panel/(1000)
    output = predictions.tolist()
    return render_template('index.html', prediction_text='Predicted Energy: kWh {}'.format(output))
​
# login end point
@app.route('/login', methods=['POST','GET'])
​
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customer where name=? and password=?",(name,password))
        data=cur.fetchone()
​
        if data:
            session["name"]=data["name"]
            session["password"]=data["password"]
            return redirect("index.html")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("login"))
​
# route when log out clicked - rediracts to home page
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('pid', None)
    session.pop('mail', None)
    return redirect(url_for('home'))
# route when sign up clicked - rediracts to register page

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            mail=request.form['mail']
            contact=request.form['password']
            address=request.form['address']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into customer(name,mail,password,address)values(?,?,?,?)",(name,mail,contact,address))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("login"))
            
            con.close()
​
    return render_template('login.html')
# route when history is clicked - navigates to history page
@app.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('history')
​
​
​
​
if __name__ == "__main__":
    app.run(debug=True)