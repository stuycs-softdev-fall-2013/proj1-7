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
@app.route("/home-popular", methods = ['GET', 'POST'])
@app.route("/home-recent/page/<page_num>", methods = ['GET', 'POST'])
@app.route("/home-popular/page/<page_num>", methods = ['GET', 'POST'])
def home(page_num=1):
	page_num = int(page_num)

	d = {}

	if request.path.find('home-recent') != -1:
		d['order'] = 'recent'
	else:
		d['order'] = 'popular'

	path = request.base_url
	d['stories'] = auth.get_stories(d['order'], page_num)
	d['error'] = False
	d['loggedIn'] = False
	d['path'] = path[:path.rfind('/')]
	d['page_num'] = page_num
	d['num_pages'] = auth.get_num_pages()
			
	if 'user' in session:
		d['loggedIn'] = True
		d['usern'] = session['user']
		return render_template("home.html", d=d)

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
		if handle_login(request.form):
			render_template

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

@app.route('/upvote/<story_id>')
def upvote(story_id):
	if 'user' in session:
		auth.upvote(session['user'], story_id)

	return redirect(url_for('home'))

@app.route('/downvote/<story_id>')
def downvote(story_id):
	if 'user' in session:
		auth.downvote(session['user'], story_id)

	return redirect(url_for('home'))

if __name__ == "__main__":
	app.debug = True
	app.run()
