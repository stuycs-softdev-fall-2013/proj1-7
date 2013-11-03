#!/usr/bin/python
#!flask/bin/python

# PROJECT: STORYINATOR 
# TITLE: BUILD - A - STORY 
# TEAM: JACK CAHN, TAK CHI WAN, JUDY MAI, BRIAN CHUCK 

#Import necessary directories
from flask import Flask
from flask import request
from flask import url_for,render_template
from flask import session,request,redirect

app = Flask(__name__)
app.secret_key="secret_key"
app.config['SHELVE_FILENAME'] = 'my_users.db'

@app.route("/")
def home():
    #return render_template('home.html')
    return "<h1> Home </h1>"; 

@app.route("/about")
def about():
    #return render_template('about.html')
    return "<h1>About</h1>"

@app.route("/login")
def login():
    #return render_template('login.html')
    return "<h1>Login</h1>"

@app.route("/register",methods=['GET', 'POST'])
def register():
    #return render_template('register.html')
    return "<h1>Register</h1>"

@app.route("/profile",methods=['GET', 'POST'])
def profile():
    #return render_template('profile.html')
    return "<h1>Profile</h1>"

@app.route("/search",methods=['GET', 'POST'])
def search():
    #return render_template('search.html')
    return "<h1>Search</h1>"

@app.route("/readStories",methods=['GET', 'POST'])
def readStories():
    #return render_template('readStories.html')
    return "<h1>Read Stories</h1>"

@app.route("/logout",methods=['GET', 'POST'])
def logout():
    #return render_template('logout.html')
    return "<h1> Logout </h1>"

@app.route("/myStories",methods=['GET', 'POST'])
def myStories():
    #return render_template('myStories.html')
    return "<h1> My Stories </h1>"

@app.route("/followedStories",methods=['GET', 'POST'])
def followedStories():
    #return render_template('followStories.html')
    return "<h1> My Folowed Stories </h1>"

@app.route("/createStories",methods=['GET', 'POST'])
def createStories():
    #return render_template('createStories.html')
    return "<h1> Create Stories </h1>"

@app.route("/createMadlibs",methods=['GET', 'POST'])
def createMadlibs():
    #return render_template('createMadlibs.html')
    return "<h1> Create Madlibs </h1>"

@app.route("/fillMadlibs",methods=['GET', 'POST'])
def fillMadlibs():
    #return render_template('fillMadlibs.html')
    return "<h1> Fill Madlibs </h1>"

@app.route("/changePass",methods=['GET','POST'])
def changePass():
    #return render_template('changePass.html')
    return "<h1> Change Password </h1>"

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5005)
