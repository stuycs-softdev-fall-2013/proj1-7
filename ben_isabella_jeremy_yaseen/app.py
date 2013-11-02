from flask import Flask, render_template, session, redirect, request, url_for
from models import User, Post, Comment
import utils

app = Flask(__name__)
users = User()
posts = Post()
comms = Comment()


""" 1) Get the latest posts and pass them to a template.
    2) Let the template know (through a boolean variable),
    whether or not a user is logged in."""
@app.route("/")
def home():
    pass


""" 1) If user is already in session, go home.
    2) If method is GET, render the login template
    3) If method is POST, check the form submissions
        - grab a list of users with the name and password using users.find(**kwargs)
        - check if the length of the list is greater than 0
        - if it is, put the username in session""" 
@app.route("/login", methods=["POST","GET"])
def login():
    if "username" in session:
        return redirect("/")
    else:
        if request.method=="GET":
            return render_template("login.html")
        else:
            username=request.form["username"].encode("ascii","ignore")
            password=request.form["password"].encode("ascii","ignore")
            if users.exists(self, name):
                if len(users.find(username=username, password=password)) > 0:
                    session["username"]=username
                    return redirect("/")
                else:
                    return redirect("/login")
            else:
                return redirect("/register")


""" 1) If users is already in session, go home.
    2) If method is GET, render the register template
    3) If method POST, check the form submissions
        - grab a list of the users with the name using users.find(**kwargs)
        - check if the length of the list is greater than 0
        - if it ISN'T, register the user using users.insert(**kwargs)"""
@app.route("/register", methods=["POST","GET"])
def register():
    if "username" in session:
        return redirect("/")
    else:
        if request.method=="GET":
            return render_template("register.html")
        else:
            username=request.form["username"].encode("ascii","ignore")
            password=request.form["password"].encode("ascii","ignore")
            if request.form["button"]=="Submit":
                if users.exists(self,username):
                    return render_template("register.html")
                else:
                    users.insert(date=datetime.now(), username=username, password=password)
                    session["username"]=username
                    return redirect("/")
            else:
                return render_template("register.html")

""" Already done"""
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect("/login")

@app.route("/change", methods=["GET","POST"])
def change():
    if request.method=="GET":
        return render_template("change.html")
    else:
        username=request.form["username"].encode("ascii","ignore")
        oldPw=request.form["old password"].encode("ascii","ignore")
        newPw=request.form["new password"].encode("ascii","ignore")
        if users.exists(self, username):
            users.find_one(username=username).change_password(self,oldPw,newPw)
        else:
            return render_template("change.html")
            

""" 1) Method should be GET
    2) Get a user with that name using users.find_one(**kwargs)
    3) If the user exists, then pass the user to the user template"""
@app.route("/users/<user>", methods=["GET","POST"])
def user_page(user):
    u=users.find_one(user)
    if users.exists(self,user):
        return render_template()
    else:
        return redirect("/")


""" 1) Same method as above, but for posts.find_one(**kwargs)
    2) If method is POST (comments added)...
        a. get the comments from the form
        b. add the comment using comms.insert(**kwargs)
        c. see test.py for how to do this"""
@app.route("/posts/<id>", methods=["GET","POST"])
def post(id):
    pass


""" 1) Get the post using posts.find_one(**kwargs)
    2) Replace kwargs with author and date
    3) redirect to url_for('post'), passing the id of the post that you just
    got"""
@app.route("/posts/<author>/<date>")
def post_by_author(author, date):
    pass


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
        if request.method=="GET":
            return render_template("create_post.html")
        else:
            title=request.form["title"]
            body=request.form["body"]
            tags=request.form["tags"]
            u = request.session["username"]
            u.add_post(date=datetime.now(),title=title,body=body,tags=tags)
    else:
        return redirect("/")


""" 1) Grab the keyword in url from request object (request.args)
    2) Get search results using utils.search(keyword)
    3) If there are no results, send a boolean letting the template know
    4) If there are results, pass the results to the search_results template"""
@app.route("/search")
def search():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
