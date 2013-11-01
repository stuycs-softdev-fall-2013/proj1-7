from flask import Flask, render_template, session, request, redirect, url_for
import auth

app = Flask(__name__)
app.secret_key = "secret key"

@app.route("/", methods = ['GET','POST'])
@app.route("/home", methods = ['GET', 'POST']) 
def home():
    if request.method == 'GET':
        if 'user' in session:
            return render_template("home.html", loggedIn = True, error = False)
        else:
            return render_template("home.html", loggedIn = False, error = False)
    else:
        if request.form['button'] == "Register":
            return render_template("register.html", message = "")
        elif request.form['button'] == "Log in":
            if auth.login(request.form['username'], request.form['password']):
                return render_template("home.html", loggedIn = True, error = False)
            else:
                return render_template("home.html", loggedIn = False, error = True)
    
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif auth.auth(username, password):
        session['user'] = username;
        return redirect(url_for('home'))
    else:
        return render_template("login.html")
        

if __name__ == "__main__":
    app.debug = True
    app.run()
