#include /usr/bin/python

from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    # home. should link to other pages
    pass

@app.route("/login")
def login():
    # login user
    pass

@app.route("/register")
def register():
    # register user
    # create user page
    pass

@app.route("/index")
def index():
    # list of blog posts
    # link to each post
    pass

@app.route("/viewpost")
def viewpost():
    # look at post x
    # load comments
    # add comments
    pass

@app.route("/writepost")
def writepost():
    # if logged in, create a new post
    # else, redirect to login
    pass

@app.route("/deletepost")
def deletepost():
    # if logged in, delete your own posts
    # if admin, delete any post
    # else, redirect to login
    pass

@app.route("/userpage")
def userpage():
    # if logged in, display your username, posts, and comments
    # else, redirect to login
    pass
    
if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=7777)
