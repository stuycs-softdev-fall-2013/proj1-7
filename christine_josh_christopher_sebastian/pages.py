from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage_loggedout(stories):
    stories = [
            {
                "id":1234,
                "title":"Banana",
                "description":"Killer Bananas Attack Things"
            },
            {
                "id":5634,
                "title":"Once Upon a Time...",
                "description":"Once Upon a Time, in the magical land of..."
            },
            {
                "id":1237,
                "title":"The End of Time",
                "description":"Doom approaches..."
            },
            {
                "id":1238,
                "title":"Blah Blah",
                "description":"blah"
            }
            ]
    return render_template('home.html', stories=stories);

def homepage_loggedin(stories, user):
    pass

def logout():
    pass

def login():
    pass

def register():
    pass

def stories(storyid):
    pass

def profile(userid):
    pass


if __name__ == '__main__':
    app.debug = True;
    app.run();
