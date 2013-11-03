#!/usr/local/bin/python
#THIS IS FOR PURPOSES OF TESTING JINJA INHERITANCE
from flask import Flask, render_template, session, redirect, request, url_for

app = Flask(__name__)

u={"username":"YaseenMe"}

@app.route("/login")
def home():
    return render_template("login.html", error="badlogin")

@app.route("/")
def hoome():
    return render_template("index.html")

@app.route("/register")
def signup():
    return render_template("register.html", error="alreadyregistered")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
