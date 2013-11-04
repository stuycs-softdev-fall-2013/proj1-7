from flask import Flask, render_template, request, session, redirect, url_for
from datagrab import *

app = Flask(__name__)

app.secret_key = "supersecretkey"

@app.route('/')
def homepage():
    logged_in = 'username' in session
    stories = []
    for story in getAllStories():
        storyData = getStory(story[1])
        stories.append({
                "id":story[1],
                "title":story[0],
                "description":storyData[0][0]
            })

    return render_template('home.html', stories=stories, logged_in=logged_in, debug=stories)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html');
    else:
        if authenticate(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Incorrect username or password");

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if request.form['password'] == request.form['confirm']:
            if addUser(request.form['username'], request.form['password']):
                return redirect(url_for('login'))
            else:
                return render_template('register.html', error="Username is already taken")
        else:
            return render_template('register.html', error="Passwords do not match")

@app.route('/stories/<int:storyid>', methods=['GET', 'POST'])
def stories(storyid):
    if request.method == 'POST':
        if 'username' in session: # check if they're logged in
            ret = newEdit(storyid, request.form['text'], session['username'])
        else:
            return redirect(url_for('login')) # they need to log in
        if ret != None:
            return redirect(url_for("stories", storyid=ret))
    story = {
            "id":storyid,
            "title":getStoryTitle(storyid),
            "content":getStory(storyid)
            }
    if story["content"] == None:
        return render_template('storynotfound.html');



    return render_template('story.html', story=story, logged_in=('username' in session), debug=story)

@app.route('/profile')
def profile(userid=0):
    return render_template('profile.html', logged_in=('username' in session))

#Old Fork:
#@app.route('/stories/fork/<int:storyid>/<int:editid>')
#def fork(storyid, editid):
#	newstoryid = newStory('title', storyid, session['username'], editid)
#	return redirect(url_for("stories", storyid=newstoryid))

@app.route('/stories/fork/<int:storyid>/<int:editid>')
def fork(storyid, editid):
	if request.method == 'POST':
		if 'username' in session:
			nS = newStory(request.form['newtitle'], storyid, session['username'], editid)
			return redirect(url_for("stories", storyid=nS))
		else:
			return redirect(url_for('login'))
		if nS != None:
			return redirect(url_for("stories", storyid=nS))
	story = {
		"id":storyid,
		"title":getStoryTitle(storyid),
		"content":getStory(storyid)
		}
	if story['content'] == None:
		return render_template('storynotfound.html');
	
	return render_template('fork.html', story=story, logged_in=('username' in session), debug=story)
	

@app.route('/dumbass')
def dumbass():
	return redirect(url_for("register"))

if __name__ == '__main__':
    createDB()
    app.debug = True;
    app.run();
