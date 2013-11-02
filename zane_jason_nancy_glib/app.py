from flask import Flask, render_template, session, request, redirect, url_for
import auth

app = Flask(__name__)
app.secret_key = 'secret key'

def getInfo():
    username = request.form['username']
    passw = request.form['password']
    return username, passw

@app.route("/", methods = ['GET', 'POST'])
def home():
    stories = auth.getStories()
    if 'user' in session:
        return render_template("home.html", loggedIn=True, error=False, stories=stories)

    if request.method == 'GET':
        return render_template("home.html", loggedIn=False, error=False, stories=stories)

    if request.form['button'] == 'Log in':
        user, pw = getInfo()
        if auth.login(user, pw):
            session['user'] = user
            return render_template("home.html", loggedIn=True, error=False, stories=stories)
		
         #login failure
        return render_template("home.html", loggedIn=False, error=True, stories=stories)

    if request.form['button'] == 'Register':
        return redirect(url_for('register'))
        
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html", error = False)
    else:
        user, pw = getInfo()
        if auth.register(user,pw):
            session['user'] = user
            return redirect(url_for('home'))
        else:
            return render_template("register.html", error = True)

@app.route("/story/<title>")
def story(title): 
    loggedIn=False
    if 'user' in session:
        loggedIn=True
    story = auth.getStory(title)
    return render_template("story.html", title=title, story=story, loggedIn=loggedIn)

@app.route("/create", methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template("create.html", loggedIn=True)
    else:
        title = request.form['title']
        story = request.form['story']
        author = session['user']
        auth.create(author, title, story)
        return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route("/account", methods =['GET', 'POST'])
def account():
    if 'user' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template("account.html", error = False, success = False, loggedIn = True)
    else:
        user = session['user']
        pw = request.form['pw']
        npw = request.form['npw']
        if auth.changePass(user,pw, npw):
            return render_template("account.html", error = False, success = True, loggedIn = True)
        else:
            return render_template("account.html", error = True, success = False, loggedIn = True)

if __name__ == "__main__":
    app.debug = True
    app.run()
