from flask import Flask, session, redirect, request, url_for
import auth

@app.route("/")
def home():
    pass

@app.route("/getuser/<user>/")
def getuser(user=None):
    pass

@app.route("/post/<author>/<date>")
def post(author=None,date=None):
    pass

@app.route("/login", methods=["POST","GET"])
def login():
    pass

@app.route("/register")
def register():
    pass

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect("/login")

@app.route("/addpost")
def addpost():
    pass
