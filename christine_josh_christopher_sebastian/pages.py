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

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/stories/<int:storyid>')
def stories(storyid):
    story= {
            "title": "The Title",
            "content": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean non interdum augue, quis imperdiet magna. Maecenas dui magna, pulvinar id interdum at, placerat vel augue. Sed eros magna, venenatis at elementum ac, rutrum vitae nisi. Nulla mollis ante felis, quis gravida quam interdum a. Proin et eros id justo aliquet malesuada sit amet eu mauris. Sed sed lacus interdum, sodales mi ut, congue magna. Donec ultricies lacinia justo, id dapibus odio porta
            adipiscing. Donec in est facilisis, rutrum metus eget, imperdiet neque. Fusce ut aliquam mauris. Ut sit amet sagittis urna. Maecenas lacus risus, aliquam ac mauris eget, facilisis aliquam justo. Suspendisse viverra iaculis tristique. Nunc pretium gravida lectus id pretium. Vivamus ut elit et nibh volutpat dapibus.

            Donec euismod mauris ut ligula venenatis bibendum. Aliquam fringilla, nulla nec convallis fermentum, urna nisi convallis massa, non pellentesque metus arcu vitae eros. Donec in pellentesque lorem. Duis dolor diam, consequat id blandit a, volutpat et nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus eu dictum ligula. Mauris egestas dui semper lorem laoreet, sed semper diam porttitor. Ut viverra imperdiet elit, sit amet
            blandit felis dapibus non. Aenean non nibh eget nulla placerat feugiat a id tellus. Praesent eget tempus velit, quis hendrerit mauris.

            Nam faucibus luctus suscipit. Nunc eleifend mattis sapien, tristique pulvinar dui congue ut. Donec et mollis risus. Mauris enim diam, faucibus in accumsan id, lacinia eu urna. Etiam id laoreet urna. In tempor fringilla elit nec porta. Quisque ornare, arcu sed accumsan convallis, mauris ante euismod lacus, id iaculis lectus massa sed augue. Donec cursus in lectus dictum ultricies. Nunc ut mattis dui. Proin ullamcorper nec ipsum eget eleifend. Morbi eget nibh adipiscing,
            blandit magna vel, bibendum leo. Ut volutpat purus nec elementum sollicitudin. Proin porttitor sapien lacus, quis volutpat elit fermentum vitae.

            Aliquam mattis malesuada nisl vel dictum. Ut pulvinar rutrum tortor, at posuere nisl faucibus sed. Fusce ornare egestas felis a mollis. Donec at aliquet leo. Integer scelerisque velit non lorem egestas sollicitudin. Morbi non magna mattis, aliquam lorem non, eleifend nulla. Aenean tortor diam, pellentesque sit amet commodo sit amet, pharetra vitae elit. Cras ornare eget ipsum eget ullamcorper. Duis aliquam urna quis libero aliquam, sed porta metus rhoncus.

            Mauris nibh nisl, ultrices a scelerisque nec, tempus in est. Donec aliquam nisi a lorem cursus, eu auctor velit sollicitudin. Suspendisse eleifend ante ornare suscipit sollicitudin. Cras vel hendrerit quam. Donec facilisis dolor dui, eu consequat nulla luctus sit amet. Nullam ante tellus, tincidunt in ultricies in, malesuada eget ipsum. Vivamus eget bibendum turpis, at rhoncus sapien. Etiam adipiscing at neque non luctus. Phasellus vestibulum euismod justo quis molestie.
            Mauris nec eleifend elit, suscipit cursus ligula.""".replace('\n', '<p>')
            }
    return render_template('story.html', story=story)

@app.route('/profile')
def profile(userid=0):
    return render_template('profile.html')


if __name__ == '__main__':
    app.debug = True;
    app.run();
