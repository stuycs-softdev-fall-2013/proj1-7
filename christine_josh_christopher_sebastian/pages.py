from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage_loggedout():
    stories = [
            {
                "id":1234,
                "title":"Banana Story",
                "description":"The Killer Bananas Attack Things..."
            },
            {
                "id":1235,
                "title":"The Dino attack",
                "description":"Attacked by dinosaurs ....."
            },
            {
                "id":5632,
                "title":"Quotes from Stuy",
                "description":"Stuy teachers on their good days..."
            },
            {
                "id":1236,
                "title":"Once Upon a Time...",
                "description":"Once Upon a Time, in the magical land of..."
            },
            
            {
                "id":1237,
                "title":"The End of Time",
                "description":"Doom approaches..."
            },
           
            ]
    return render_template('home.html', stories=stories);

def homepage_loggedin(stories, user):
    pass

def logout():
    pass

@app.route('/login')
def login():
    return render_template('login.html');

def register():
    pass

def stories(storyid):
    pass

def profile(userid):
    pass


if __name__ == '__main__':
    app.debug = True;
    app.run();
