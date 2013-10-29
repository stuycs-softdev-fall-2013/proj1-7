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
    pass

@app.route("/index")
def index():
    # list of blog posts
    pass

@app.route("post1")
def post1():
    # look at post 1
    pass

@app.route("/writepost")
def writepost():
    # if admin, create a new post
    # else, redirect somewhere
    pass
    
if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=7777)
