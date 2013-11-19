#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
from bson import ObjectId
from models import User, Post, Comment
from settings import SECRET_KEY
import subprocess
import es

app = Flask(__name__)
app.secret_key = SECRET_KEY
users = User()
posts = Post()
comms = Comment()


# Home page: displays newest posts
@app.route("/")
def home():
    sort = request.args.get("sort")
    if sort == "mostvoted":
        target_posts = posts.get_most_voted()
    else:
        target_posts = posts.get_by_date()
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        return render_template("index.html", posts=target_posts, user=u)
    return render_template("index.html", posts=target_posts)


# Login page
@app.route("/login", methods=["POST", "GET"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        if request.method == "GET":
            return render_template("login.html")
        else:
            username = request.form["username"]
            password = request.form["password"]
            if users.exists(username):
                if users.find_one(username=username, password=password):
                    session["username"] = username
                    return redirect(url_for("home"))
                else:
                    return render_template("login.html", error="badlogin")
            else:
                return redirect(url_for("register"))


# Register page
@app.route("/register", methods=["POST","GET"])
def register():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        if request.method == "GET":
            return render_template("register.html")
        else:
            username = request.form["username"]
            password = request.form["password"]
            cpass = request.form["confirm password"]
            if users.exists(username) and password == cpass:
                return render_template("register.html", error="alreadyregistered")
            elif username == "":
                return render_template("register.html", error="noname")
            elif password == "":
                return render_template("register.html", error="nopassword")
            else:
                users.insert(username=username, password=password)
                session["username"] = username
                return redirect(url_for("home"))


# Link to logout
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))


# Change password page
@app.route("/change", methods=["GET","POST"])
def change():
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        if request.method == "GET":
            return render_template("change.html", user=u)
        else:
            oldpw = request.form["old-password"]
            newpw = request.form["new-password"]
            newpw2= request.form["new-password-2"]
            if newpw==newpw2:
                if u.change_password(oldpw, newpw):
                    return redirect(url_for("home"))
                else:
                    #Add some error message
                    return render_template("change.html", user=u, error="old-password-incorrect")
            else:
                #Second error
                return render_template("change.html", user=u, error="new-password-no-match")


# Page for a specified user
@app.route("/users/<user>", methods=["GET"])
def user_page(user):
    if users.exists(user):
        target_user = users.find_one(username=user)
        p=target_user.get_posts()
        if "username" in session:
            username = session["username"]
            u = users.find_one(username=username)
            return render_template("user.html",target_user=target_user, posts=p, user=u)
        return render_template("user.html",target_user=target_user, posts=p)
    else:
        return redirect(url_for("home"))


# Page for a specified post
@app.route("/posts/<id>", methods=["GET","POST"])
def post(id):
    p = posts.find_one(_id=ObjectId(id))
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        if request.method == "GET":
            return render_template("post.html", post=p, user=u)
        else:
            #I'm assuming you can only comment if you're logged in
            comment = request.form["comment"].replace("\n", "<br>")
            p.add_comment(user=username, text=comment)
            return render_template("post.html", post=p, user=u)
    else:
        return render_template("post.html", post=p)


# Same as above
@app.route("/posts/<author>/<date>")
def post_by_author(author, date):
    target_post = posts.find_one(author=author, date=date)
    return redirect(url_for("post", id=target_post.get_id()))


@app.route("/vote-up")
def vote_up():
    last_page = request.args.get("last")
    if "username" in session:
        pid = request.args.get("pid")
        username = session["username"]
        u = users.find_one(username=username)
        u.vote_up(ObjectId(pid))
    return redirect(last_page)


# Remoeve a post
@app.route("/remove-post")
def remove_post():
    pid = request.args.get("pid")
    posts.remove(_id=ObjectId(pid))
    return redirect(url_for("home"))


# Page to create a post
@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        if request.method == "GET":
            return render_template("create_post.html", user=u)
        else:
            title = request.form["title"]
            body = request.form["body"].replace("\n", "<br>")
            tags = request.form["tags"].lower().split(' ')
            p = u.add_post(title=title, body=body, tags=tags)
            return redirect(url_for("post", id=p.get_id()))
    else:
        return redirect(url_for("home"))


# Search results page
@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    results = es.search(keyword)
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        return render_template("search_results.html", results=results, keyword=keyword, user=u)
    return render_template("search_results.html", results=results, keyword=keyword)


if __name__ == '__main__':
    subprocess.Popen(['elasticsearch'])
    subprocess.Popen(['./es.py'])
    app.run(debug=True, host='0.0.0.0', port=5000)
