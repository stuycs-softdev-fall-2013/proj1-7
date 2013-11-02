from flask import Flask, render_template, session, request, redirect, url_for, session

import db

app = Flask(__name__)
app.secret_key = "KEHTYSOEIETIRRUVSERSCY"

@app.route('/')
def home():
    logged_in = False
    username = ''
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
        if request.form['username'] == request.form['pw_verify']:
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
    return redirect('/u/'+session['username'])
    #list of user's stories

@app.route('/story/<title>', methods=['GET','POST'])
def story(title):
    if request.method == 'GET':
        pass
        #check that the story hasn't been edited by user yet
        #returns page with the story and edit box if not edited yet
    #returns page with the story

@app.route('/u/<usern>')
def profile(usern):
    stories = [db.get_title(sid) for sid in db.stories_for_user(usern)]
    return render_template('user.html', username=usern, stories=stories)

if __name__ == '__main__':
    app.debug = True
    app.run()
