from flask import Flask
from flask import render_template, session, request, redirect, url_for
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

@app.route("/story/<eyed>")
def story(eyed): 
    loggedIn=False
    if 'user' in session:
        loggedIn=True
    author, title, story = auth.getStory(eyed)
    if request.method == "POST":
        line = request.form['lines']
        auth.add(id, lines)
    return render_template("story.html", author=author, title=title, story=story, loggedIn=loggedIn)

@app.route("/profile/<id>")
def profile(id):
    d['loggedIn'] = False
    if 'user' in session:
        d['loggedIn'] = True
    user,made,contrib = auth.getInfo(id)
    for s in made:
        s['title'] = auth.getTitle(s['id'])
    for s in contrib:
        s['title'] = auth.getTitle(s['id'])
    d['owned_stories'] = made
    d['contrib_stories'] = contrib
    return render_template("profile.html", user=user, d=d)

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
	
	d = {}
	d['loggedIn'] = True

	if request.method == 'GET':
   		d['error'] = False
    	d['success'] = False
    	return render_template("account.html", d=d)

	#POST
	user = session['user']
	pw = request.form['pw']
	npw = request.form['npw']
	npwcf = request.form['npwcf']
	if npw == npwcf and auth.changePass(user, pw, npw):
            d['success'] = True
            return render_template("account.html", d=d)
	else:
		d['error'] = True
		d['success'] = False
		return render_template("account.html", d=d)

if __name__ == "__main__":
	app.debug = True
	app.run()
