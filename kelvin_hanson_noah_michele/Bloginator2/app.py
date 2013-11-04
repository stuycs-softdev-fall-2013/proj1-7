from flask import Flask, session, redirect, request, url_for, render_template
import auth
import posts
import comments
import datetime

app = Flask(__name__)
app.secret_key = 'secret'
d= {}
@app.route('/')
def home():
    if 'username' in session:
        user = session['username']
    else:
        user = "Guest"
    return render_template('home.html', Username = user)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if 'username' in session:
        username = session['username']
        if request.method == "GET":
            return render_template('create.html')
        title = request.form['title']
        post = request.form['post']
        date = datetime.datetime.now();
        posts.addPost(username, title, post,date)
        return render_template('create.html')
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html')
    username = request.form['Username']
    password = request.form['Password']
    if auth.auth(username,password):
        session['username']=username
        return redirect(url_for('home'))
    return render_template('login.html', 
                           message = 'Invalid combo')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('register.html')
    username = request.form['Username']
    password = request.form['Password']
    cpassword = request.form['CPassword']
    if auth.exists(username):
        return render_template('register.html',
                               message='Username already exists')
    if password != cpassword:
        return render_template('register.html',
                               message='Passwords do not match')
    auth.addUser(username, password)
    return redirect(url_for('home'))

@app.route('/blog')
def blog():
    if 'username' in session:
        user = session['username']
    else:
        user = "Guest"
    return render_template("blog.html", username = user, post = posts.getPosts())


@app.route('/blog/<title>', methods = ['GET', 'POST'])
def post(title):
    blogPost = posts.getPost( title)
    datetime = getPostTime(title)
    return render_template("blogtemplate.html", title=title, post=blogPost, date=datetime)
    
@app.route('/blog/<title>/comments')
def comments(title):
     comments = comments.getComments(title)
     return render_template("commenttemplate.html", title=title, comment=comments)

@app.route('/blog/<title>/submit', methods = ['GET','POST'])
def submit(title):
    if 'username' in session:
        user = session['username']
    else:
        user = "Guest"
    if request.method == GET:
        return render_template("submit.html")
    comment = request.form['Comment']
    comments.addComment(user, title, comment)
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port =5000)
                        
                    
