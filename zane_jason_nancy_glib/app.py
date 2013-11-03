from flask import Flask
from flask import render_template, session, request, redirect, url_for
import auth2 as auth

app = Flask(__name__)
app.secret_key = 'secret key'

def getInfo():
	username = request.form['username']
	passw = request.form['password']
	return username, passw

@app.route("/", methods = ['GET', 'POST'])
@app.route("/page/<page_num>", methods = ['GET', 'POST'])
@app.route("/home-recent", methods = ['GET', 'POST'])
@app.route("/home-recent/page/<page_num>", methods = ['GET', 'POST'])
def home(page_num=1):
	d = {}

	if request.path.find('home-recent') != -1:
		d['order'] = 'recent'
	else:
		d['order'] = 'popular'

	d['stories'] = auth.get_stories(d['order'], page_num)
	d['error'] = False
	d['loggedIn'] = False
			
	if 'user' in session:
		d['loggedIn'] = True
		return render_template("home.html", d=d)

	if request.method == 'GET':
		return render_template("home.html", d=d)

	if request.form['button'] == 'Log in':
		user, pw = getInfo()

		if auth.login(user, pw):
			session['user'] = user
			d['loggedIn'] = True
			return render_template("home.html", d=d)
		
		#login failure
		d['error'] = True
		return render_template("home.html", d=d)

	if request.form['button'] == 'Register':
		return redirect(url_for('register'))
		
@app.route("/register", methods = ['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template("register.html", error = False)

	#POST
	usern = request.form['username']
	passw = request.form['password']
	passwcf = request.form['password-confirm']

	if auth.register(usern, passw, passwcf):
		session['user'] = usern
		return redirect(url_for('home'))

	return render_template("register.html", error = True)

@app.route("/story/<story_id>", methods=['GET','POST'])
def story(story_id): 
	loggedIn = 'user' in session

	story = auth.get_story(story_id)
	
	if request.method == "POST":
		lines = request.form['lines']
		auth.add(eyed, lines, session['user'],title)

	return render_template("story.html", story=story)

@app.route("/profile/<eyed>")
def profile(eyed):
	d = {'loggedIn': 'user' in session}

	user,made,contrib = auth.getInfo(eyed)

	for s in made:
		s['title'] = auth.getTitle(s['eyed'])

	for s in contrib:
		s['title'] = auth.getTitle(s['eyed'])

	d['owned_stories'] = made
	d['contrib_stories'] = contrib
	
	return render_template("profile.html", user=user, d=d)

@app.route("/create", methods=['GET', 'POST'])
def create():
	if 'user' not in session:
		return redirect(url_for('home'))

	if request.method == 'GET':
		return render_template("create.html", loggedIn=True)

	#POST
	title = request.form['title']
	story = request.form['story']
	author = session['user']

	auth.create_story(author, title, story)

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
