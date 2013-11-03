from flask import Flask, render_template, session, request, redirect, url_for, session

import db

app = Flask(__name__)
app.secret_key = "KEHTYSOEIETIRRUVSERSCY"

@app.route('/')
def home():
    logged_in = False
    name = ''
    if 'username' in session:
        logged_in = True
        username = session['username']
    #list of newest stories
    if 'username' in session:
        return render_template("homepage.html",link="link to user's stories")
    else:
        return render_template("homepage.html",link="link to register/sign in page")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        #return register page
        return render_template('register.html');
    else:
        if request.form['password'] != request.form['pw_verify']:
            print request.form['username'], request.form['pw_verify']
            return render_template('register.html', error='Passwords do not match')
        if db.register_user(request.form['username'],request.form['password']):
            #redirect to home? sign in?
            return redirect(url_for('home'))
        else:
            #redirect to same page with an error message
            return render_template('register.html', error='Username already exists')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template("login.html")
    else:
        if db.check_user(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Wrong username/password combination")
            #redirect to same page with an error message

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))

@app.route('/passchange', methods=['GET','POST'])
def passchange():
    if request.method == 'GET':
        #return password change page
        pass
    elif change_pass(request.form['username'],request.form['password']):
        pass
        #return password change success page
    else:
        pass
        #redirect to same page with an error message

@app.route('/stories')
def stories():
    if 'username' in session:
        return redirect('/u/'+session['username'])
    else:
        return redirect(url_for('login'))
    #list of user's stories

@app.route('/story/<title>', methods=['GET','POST'])
def story(title):
    if request.method == 'GET':
        sid = db.get_storyid(title)
        return "<h1>%s</h1>%s"%(db.get_title(sid), db.get_story(sid))
        #check that the story hasn't been edited by user yet
        #returns page with the story and edit box if not edited yet
    #returns page with the story

@app.route('/u/<usern>')
def profile(usern):
    originals = [db.get_title(sid) for sid in db.stories_by_user(usern)]
    contributed = [(len(db.contributions_to_story(usern, sid)), db.get_title(sid)) for sid in db.stories_with_user_contributions(usern)]
    print "contributions", db.contributions_to_story(usern, db.stories_by_user(usern)[0])
    contributed.sort(reverse=True)
    return render_template('user.html', username=usern, originals=originals, contribs=contributed)

@app.route('/write')
def write():
	#TODO:
	##pick a random story
	##allow user to write one line
	##templates/writePage.html
	pass

@app.route('/add')
def add():
	#TODO:
	##allow usere to submit a title
	##add a new contributable story with that title
	##templates/addPage.html
	pass

if __name__ == '__main__':
    app.debug = True
    app.run()
