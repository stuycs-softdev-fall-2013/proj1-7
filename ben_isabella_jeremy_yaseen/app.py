#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
from models import User, Post, Comment
import utils

app = Flask(__name__)
users = User()
posts = Post()
comms = Comment()


""" 1) Get the latest posts and pass them to a template.
    2) Let the template know whether or not a user is logged in."""
@app.route("/")
def home():
    ordered_posts = posts.get_by_date()
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        return render_template("index.html", posts=ordered_posts, user=u)
    return render_template("index.html", posts=ordered_posts)


""" 1) If user is already in session, go home.
    2) If method is GET, render the login template
    3) If method is POST, check the form submissions
        - grab a list of users with the name and password using users.find(**kwargs)
        - check if the length of the list is greater than 0
        - if it is, put the username in session"""
@app.route("/login", methods=["POST","GET"])
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
                    #Add some error message
                    return render_template("login.html")
            else:
                return redirect(url_for("register"))


""" 1) If users is already in session, go home.
    2) If method is GET, render the register template
    3) If method POST, check the form submissions
        - grab a list of the users with the name using users.find(**kwargs)
        - check if the length of the list is greater than 0
        - if it ISN'T, register the user using users.insert(**kwargs)"""
@app.route("/register", methods=["POST","GET"])
def register():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        if request.method == "GET":
            return render_template("register.html")
        else:
            username=request.form["username"]
            password=request.form["password"]
            if request.form["button"] == "Submit":
                if users.exists(username):
                    #Add an error message here
                    return render_template("register.html")
                else:
                    users.insert(username=username, password=password)
                    session["username"] = username
                    return redirect(url_for("home"))
            else:
                return render_template("register.html")


""" Already done"""
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))


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
            if u.change_password(oldpw, newpw):
                return redirect(url_for("home"))
            else:
                #Add some error message
                return render_template("change.html", user=u)


""" 1) Method should be GET
    2) Get a user with that name using users.find_one(**kwargs)
    3) If the user exists, then pass the user to the user template"""
@app.route("/users/<user>", methods=["GET"])
def user_page(user):
    if users.exists(user):
        target_user = users.find_one(username=user)
        if "username" in session:
            username = session["username"]
            u = users.find_one(username=username)
            return render_template(target_user=target_user, user=u)
        return render_template(target_user=target_user)
    else:
        return redirect(url_for("home"))


""" 1) Same method as above, but for posts.find_one(**kwargs)
    2) If method is POST (comments added)...
        a. get the comments from the form
        b. add the comment using comms.insert(**kwargs)
        c. see test.py for how to do this"""
@app.route("/posts/<id>", methods=["GET","POST"])
def post(id):
    p = posts.find_one(id=id)
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        if request.method == "GET":
            return render_template(post=p, user=u)
        else:
            #I'm assuming you can only comment if you're logged in
            comment = request.form["comment"]
            p.add_comment(user=u, text=comment)
            return render_template("post.html", post=p, user=u)
    else:
        return render_template("post.html", post=p)


""" 1) Get the post using posts.find_one(**kwargs)
    2) Replace kwargs with author and date
    3) redirect to url_for('post'), passing the id of the post that you just
    got"""
@app.route("/posts/<author>/<date>")
def post_by_author(author, date):
    target_post = posts.find_one(author=author, date=date)
    return redirect(url_for("post", id=target_post._id))


""" 1) If method is GET...
        a. If user is in session
            - render the create_post template
    2) If method is POST...
        b. Get the form submissions
            - insert the post with the values from the form with
            posts.insert(**kwargs)
            - Be sure to include the username, and the current date in
            posts.insert (see test.py)"""
@app.route("/create-post")
def create_post():
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        if request.method == "GET":
            return render_template("create_post.html", user=u)
        else:
            title=request.form["title"]
            body=request.form["body"]
            tags=request.form["tags"]
            p = u.add_post(title=title, body=body, tags=tags)
            return redirect(url_for("post", id=p._id))
    else:
        return redirect(url_for("home"))


""" 1) Grab the keyword in url from request object (request.args)
    2) Get search results using utils.search(keyword)
    3) If there are no results, send a boolean letting the template know
    4) If there are results, pass the results to the search_results template"""
@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    results = utils.search(keyword)
    if "username" in session:
        username = session["username"]
        u = users.find_one(username=username)
        return render_template("search_results.html", results=results, user=u)
    return render_template("search_results.html", results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
