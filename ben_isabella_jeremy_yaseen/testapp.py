#!/usr/local/bin/python
#THIS IS FOR PURPOSES OF TESTING JINJA INHERITANCE
from flask import Flask, render_template, session, redirect, request, url_for

app = Flask(__name__)

u={"username":"YaseenMe"}

_post={"title":"TITLE","user":"YaseenMe","date":"11/3/13 14:39:22","upvotes":52,"body":"THis is the body of the post"}

posts=[_post]

@app.route("/login")
def home():
    return render_template("login.html")

@app.route("/")
def hoome():
    return render_template("index.html")

@app.route("/register")
def signup():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
