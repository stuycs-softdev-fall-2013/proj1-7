#!/usr/bin/python
#!flask/bin/python

# PROJECT: STORYINATOR 
# TITLE: BUILD - A - STORY 
# TEAM: JACK CAHN, TAK CHI WAN, JUDY MAI, BRIAN CHUK

#Import necessary directories
from flask import Flask
from flask import request
from flask import url_for,render_template
from flask import session,redirect

app = Flask(__name__)
app.secret_key="secret_key"
app.config['SHELVE_FILENAME'] = 'my_users.db'
#app = Flask(__name__, static_url_path= "/templates", static_folder = "/templates")
import auth

@app.route("/")
def home():
    return render_template('index.html', Story1 = "s1", Story2 = "s1", Story3 = "s1", Story4 = "s1")

@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html", message = "")
    else:
        user = request.form['user']
        pw = request.form['pass']
        if user == "" or pw == "":
            return render_template("login.html", message = "Please enter your username and password.")
        elif auth.login(user, pw):
            session['user'] = user
            return redirect(url_for('home'))
        else:
            return render_template("login.html", message = "Invalid username and password combination. Usernames and passwords are case sensitive. Please try again.")    

@app.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html", message = "")
    else:
        button = request.form['button'].encode("utf8")
        if button == "Submit":
            if auth.register(request.form['user'], request.form['pass']):
                session['user'] = request.form['user']
                return redirect(url_for('home'))
            else:
                return render_template("register.html", message = "User already exists. Please login.")
        else:
            return render_template("register.html", message = "")    

@app.route("/profile",methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')
    return "<h1>Profile</h1>"

@app.route("/read",methods=['GET', 'POST'])
def read():
    return render_template('read.html', post = auth.findAll())

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/search",methods=['GET', 'POST'])
def search():
    return render_template('search.html')
    return "<h1>Search</h1>"

@app.route("/create",methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template("create.html", message = "")
    else:
        button = request.form['button'].encode("utf8")
        if button == "Submit":
            auth.makestory(request.form['title'], request.form['author'], request.form['Address'], request.form['date']); 
            return render_template("read.html"); 
        else:
            return render_template("create.html", message = "Please Create a Valid Story.")

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5005)
