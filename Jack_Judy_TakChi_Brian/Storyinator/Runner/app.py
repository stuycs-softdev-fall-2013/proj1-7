#!/usr/bin/python
#!flask/bin/python

#This is Jack Cahn and Alvin Leung's Project

from flask import Flask
from flask import request
from flask import url_for,render_template
from flask import session,request,redirect

from auth import authenticate, adduser

app = Flask(__name__)
app.secret_key="secret_key"
app.config['SHELVE_FILENAME'] = 'my_users.db'

@app.route("/")
def home():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route("/about")
def about():
    return "<h1>About</h1>"

@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        button = request.form['button']
        if button == 'login':
            username = request.form['username'].encode ('ascii',"ignore")
            password = request.form['password'].encode ('ascii',"ignore")
            if authenticate(username,password):
                session['username'] = username
                return redirect("/form")
            else:
                return render_template("register.html",error="Please Register. Your username does not exist")
        else:
	    return redirect("/register")
            
              
@app.route("/form",methods=['GET','POST'])
def form():
    if 'username' in session:
        if request.method=="GET":
            return render_template('form.html')
        else:
            d={'name':request.form['username'],
               'HR':request.form['HR']}
            button=request.form['button']
            if button=="complete":
                f=open("data.dat","a")
                s="%(name)s:%(HR)s\n"%(d)
                f.write(s)
                f.close()
                return render_template("render_template.html",d=d)
            else:
                return redirect("/form")
    else:
        redirect(url_for('login'))
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html",error="")
    elif request.method == 'POST':
        user = request.form['user'].encode('ascii','ignore')
        pw = request.form['pass'].encode('ascii','ignore')
        if adduser(user, pw):
            return redirect(url_for('login'))
        else: 
            return render_template("register.html",error="Username already exists")

@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5005)

@app.route("/changepw",methods=['GET','POST'])
def changepw():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('changepass.html',msg='')
        elif request.method == 'POST':
            oldpw = request.form['oldpass'].encode('ascii','ignore')
            newpw = request.form['newpass'].encode('ascii','ignore')
            if changepass(session['username'],oldpw,newpw):
                return redirect(url_for('login'))
            else:
                return render_template('changepass.html',msg='Incorrect password')
    else:
        return redirect(url_for('login'))
