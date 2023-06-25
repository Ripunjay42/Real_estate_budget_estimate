from flask import Flask,render_template,url_for,request,jsonify,redirect
from flask_cors import cross_origin,CORS
import utility
import requests
import pandas as pd
import numpy as np
import datetime
import pickle
import sklearn
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt




app = Flask(__name__, template_folder="templates")



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "secretkey12"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.init_app(app)


# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    
# Initialize app with extension
db.init_app(app)
# Create database within app context
 
with app.app_context():
    db.create_all()


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")


@app.route("/register" , methods=["GET", "POST"])
def register():
	
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                    password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login" , methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return render_template("predict.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
        logout_user()
        return render_template("index.html")

@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def predict():
        if request.method=="POST":
	            return render_template("predict.html")

@app.route('/get_location_names',methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': utility.get_location_names()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['GET','POST'])
@cross_origin()
def predict_home_price():
    Area = float(request.form['Area'])
    Location = request.form['Location']
    bhk = int(request.form['bhk'])
    New_or_Resale = int(request.form['New_or_Resale'])
    Gymnasium = int(request.form['Gymnasium'])
    Lift_Available = int(request.form['Lift_Available'])
    Car_Parking = int(request.form['Car_Parking'])
    Clubhouse = int(request.form['Clubhouse'])
    Gas_Connection = int(request.form['Gas_Connection'])
    Jogging_Track = int(request.form['Jogging_Track'])
    Swimming_Pool = int(request.form['Swimming_Pool'])
    print(request.form['Area'])

    response = jsonify({
        'estimated_price': utility.get_estimated_price(Location,Area,New_or_Resale,Gymnasium,Lift_Available,Car_Parking,Clubhouse,Gas_Connection,Jogging_Track,Swimming_Pool,bhk)
    })
    # response.headers.add("Access-Control-Allow-Origin", "")
    # response.headers.add("Access-Control-Allow-Headers", "")
    # response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == "__main__":
    print("Start Python Flask Server for Real Estate Price Prediction")
    utility.load_saved_artifacts()
    cors = CORS(app)
    # print(utility.get_location_names())
    # print(utility.get_estimated_price('Vashi',10000,0,1,0,1,1,0,1,1,2))
    app.run(debug=True)


