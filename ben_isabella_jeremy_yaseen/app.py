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
    pass


""" 1) If users is already in session, go home.
    2) If method is GET, render the register template
    3) If method POST, check the form submissions
        - grab a list of the users with the name using users.find(**kwargs)
        - check if the length of the list is greater than 0
        - if it ISN'T, register the user using users.insert(**kwargs)"""
@app.route("/register")
def register():
    pass

""" Already done"""
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect("/login")


""" 1) Method should be GET
    2) Get a user with that name using user.find_one(**kwargs)
    3) If the user exists, then pass the user to the user template"""
@app.route("/users/<user>")
def user_page(user):
    pass


""" 1) Same method as above, but for posts.find_one(**kwargs)
    2) If method is POST (comments added)...
        a. get the comments from the form
        b. add the comment using comms.insert(**kwargs)
        c. see test.py for how to do this"""
@app.route("/posts/<id>")
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
    pass


""" 1) Grab the keyword in url from request object (request.args)
    2) Get search results using utils.search(keyword)
    3) If there are no results, send a boolean letting the template know
    4) If there are results, pass the results to the search_results template"""
@app.route("/search")
def search():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
