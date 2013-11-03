import flask

from flask import Flask
app = Flask(__name__)

from post_database import PostDatabase
posts_db = PostDatabase('posts.db')

@app.route('/')
def index():
    return str(posts_db.get_posts())

@app.route('/login')
def login():
    return 'login'

@app.route('/admin')
def admin():
    return 'admin'

def main():
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
    pass
