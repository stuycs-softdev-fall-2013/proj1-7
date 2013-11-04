from flask import Flask, render_template
from datagrab import *

app = Flask(__name__)

@app.route('/')
def homepage():
    stories = []
    for story in getAllStories():
        storyData = getStory(story[1])
        stories.append({
                "id":story[1],
                "title":story[0],
                "description":storyData[0][0]
            })

    return render_template('home.html', stories=stories, debug=stories)

def logout():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html');

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/stories/<int:storyid>')
def stories(storyid):
    story = {
            "id":storyid,
            "title":"The Title",
            "content":getStory(storyid)
            }
    if story["content"] == None:
        return render_template('storynotfound.html');
    return render_template('story.html', story=story, debug=story)

@app.route('/profile')
def profile(userid=0):
    return render_template('profile.html')


if __name__ == '__main__':
    app.debug = True;
    app.run();
