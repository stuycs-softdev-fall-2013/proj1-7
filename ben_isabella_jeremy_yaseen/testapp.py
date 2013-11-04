#!/usr/local/bin/python
#THIS IS FOR PURPOSES OF TESTING JINJA INHERITANCE
from flask import Flask, render_template, session, redirect, request, url_for

app = Flask(__name__)

u={"username":"YaseenMe"}

_post={"title":"TITLE","user":"YaseenMe","date":"11/3/13 14:39:22","upvotes":52,"body":"THis is the body of the post. NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN NYAN"}

posts=[_post]

@app.route("/login")
def home():
    return render_template("login.html")

@app.route("/")
def hoome():
    return render_template("index.html", user=u)

@app.route("/register")
def signup():
    return render_template("register.html")

@app.route("/user/<user>", methods=["GET"])
def user_page(user):
    return render_template("userpage.html", target_user=u, user=u, posts=posts)

@app.route("/testpost")
def testpost():
    return render_template("post.html",user=u, post=_post)

@app.route("/search")
def search():
    return render_template("search_results.html",results=posts, keyword="swag", user=u)

@app.route("/create-post")
def createpost():
    return render_template("create_post.html", user=u)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
