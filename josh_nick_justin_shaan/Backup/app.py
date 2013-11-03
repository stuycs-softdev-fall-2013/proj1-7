import flask
from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for
from post_database import PostDatabase
from auth_database import AuthDatabase

app = Flask(__name__)
posts_db = PostDatabase('posts.db')
auth_db = AuthDatabase('auth.db')

@app.route('/')
@app.route('/index.html')
def index():
    return render_template(
        'index.html'
        posts_db.get_posts())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if auth_user(
            request.form['username'],
            request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('admin.html')
    elif request.method == 'POST':
        posts_db.add_post(
            request.form['title'],
            request.form['content'])
        return render_template('admin.html')

def main():
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
    pass
