from flask import Flask
from flask import render_template, session, request, redirect, url_for
import auth2 as auth

app = Flask(__name__)
app.secret_key = 'secret key'

def getInfo():
	username = request.form['username']
	passw = request.form['password']
	return username, passw

@app.route('/')
def root():
	return redirect(url_for('home'))

@app.route("/home-recent", methods = ['GET', 'POST'])
@app.route("/home-least-popular", methods = ['GET', 'POST'])
@app.route("/home-popular", methods = ['GET', 'POST'])
@app.route("/home-recent/page/<page_num>", methods = ['GET', 'POST'])
@app.route("/home-popular/page/<page_num>", methods = ['GET', 'POST'])
@app.route("/home-least-popular/page/<page_num>",
		   methods = ['GET', 'POST'])
def home(page_num=1):
	page_num = int(page_num)

	d = {}

	if request.path.find('home-recent') != -1:
		d['order'] = 'recent'
	elif request.path.find('home-popular') != -1:
		d['order'] = 'popular'
	else:
		d['order'] = 'least-popular'

	path = request.base_url
	d['stories'] = auth.get_stories(d['order'], page_num)
	d['error'] = False
	d['loggedIn'] = False
	d['path'] = path[:path.rfind('/')]
	d['page_num'] = page_num
	d['num_pages'] = auth.get_num_pages()
			
	if 'user' in session:
		usern = session['user']
		d['loggedIn'] = True
		d['usern'] = usern
		d['downvoted'] = auth.get_downvoted(usern)
		d['upvoted'] = auth.get_upvoted(usern)

		if request.method == "GET":
			return render_template("home.html", d=d)
		elif request.form['button'] == "Upvote":
			auth.upvote(usern, request.form['story_id'])
			return redirect(request.url)
		elif request.form['button'] == "Downvote":
			auth.downvote(usern, request.form['story_id'])
			return redirect(request.url)

	if request.method == 'GET':
		return render_template("home.html", d=d)

	if request.form['button'] == 'Log in':
		if auth.handle_login(request.form):
			d['loggedIn'] = True
			return render_template("home.html", d=d)
		
		#login failure
		d['login-failure'] = True
		return render_template("home.html", d=d)

	if request.form['button'] == 'Register':
		return redirect(url_for('register'))
		
@app.route("/register", methods = ['GET', 'POST'])
def register():
	if 'user' in session:
		return redirect(url_for('home'))

	d = {'usern-used': False,
		 'passw-mismatch': False}

	if request.method == 'GET':
		return render_template("register.html", d=d)

	#POST
	if request.form['button'] == 'Log in':
		if auth.handle_login(request.form):
			session['user'] = request.form['username']
			return redirect(url_for('home'))
		else:
			return redirect(url_for('home'))

	usern = request.form['username']
	passw = request.form['password']
	passwcf = request.form['password-confirm']

	errcode = auth.register(usern, passw, passwcf)

	if not errcode: #success
		session['user'] = usern
		return redirect(url_for('home'))

	for err in errcode:
		d[err] = True
	return render_template("register.html", d=d)

@app.route("/story/<story_id>", methods=['GET','POST'])
def story(story_id): 
	d = {'loggedIn': 'user' in session, 'usern': session['user']}

	if request.method == "POST":
		line = request.form['line']
		auth.add_line(session['user'], line, story_id)

	story = auth.get_story(story_id)
	
	return render_template("story.html", story=story, d=d)

@app.route("/profile/<usern>")
def profile(usern):
	d = {'loggedIn': 'user' in session, 'usern': session['user']}

	user = auth.get_user(usern)
	
	d['owned_stories'] = auth.get_owned_stories(usern)
	d['contrib_stories'] = auth.get_contrib_stories(usern)

	if user:	
		return render_template("profile.html", user=user, d=d)
	
	return redirect(url_for('home'))

@app.route("/create", methods=['GET', 'POST'])
def create():
	if 'user' not in session:
		return redirect(url_for('home'))

	d = {'loggedIn': True, 'usern': session['user']}

	if request.method == 'GET':
		return render_template("create.html", d=d)

	#POST
	title = request.form['title']
	story = request.form['story']
	author = session['user']

	if not title:
		d['title-error'] = True
		return render_template("create.html", d=d)

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
	
	d = {'loggedIn': True, 'usern': session['user']}

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

	d['error'] = True
	d['success'] = False
	return render_template("account.html", d=d)

if __name__ == "__main__":
	app.debug = True
	app.run()
