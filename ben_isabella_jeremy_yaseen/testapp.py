#!/usr/local/bin/python
#THIS IS FOR PURPOSES OF TESTING JINJA INHERITANCE
from flask import Flask, render_template, session, redirect, request, url_for

app = Flask(__name__)

u={"username":"ME"}

@app.route("/")
def home():
    return render_template("blogpost.html", user="none")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
