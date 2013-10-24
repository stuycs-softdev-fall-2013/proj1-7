#include /usr/bin/python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    pass

@app.route("/login")
def login():
    pass

@app.route("/register")
def register():
    pass

@app.route("/index")
def index():
    pass



if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=7777)
