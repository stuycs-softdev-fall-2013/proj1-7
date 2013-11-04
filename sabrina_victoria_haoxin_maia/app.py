import auth
import posts
from time import strftime
from flask import Flask,render_template,session,redirect,request,url_for

app = Flask(__name__)
app.secret_key = "BLOGINATOR"
_ADMIN = 'ADMIN'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('/'))
    elif request.method == 'GET':
        return render_template('Register.html')
    elif request.method == 'POST':
        fname = request.form['Firstname']
        lname = request.form['Lastname']
        name = request.form['username']
        pw = request.form['password']
        pw2 = request.form['password2']
        if auth.register(name,pw,pw2) == 0:
            return redirect(url_for('home'))
        elif auth.register(fname,lname,name,pw,pw2) == 1:
            return "username already registered. Try a different one" + render_template("Register.html")
        return "the passwords you typed do not match, please try again" + reder_template("Register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('Login.html')
    elif request.method == 'POST':
        if auth.authenticate(request.form['username'],request.form['pw']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        return "unrecognized user and/or password combination" + render_template('Login.html')

@app.route('/manage')
def manage():
    if 'username' not in session:
        return redirect(url_for('/login'))
    elif request.method == 'GET':
        return render_template('manage.html',username = session['username'])
    elif request.method == 'POST':
        pw = request.form['oldPassWord']
        newpw = request.form['newPassWord']
        newpw2 = request.form['newPassWord2']
        if not auth.authenticate(session['username'],pw):
            return "incorrect current password" + render_template('manage.html')
        elif newpw != newpw2:
            return "new passwords do not match" + render_template('manage.html')
        else:
            auth.changepw(session['username'],newpw)
            return redirect(url_for('myacc'))

@app.route('/myacc',methods=['GET','POST'])
def myacc():
    if 'username' in session:
        name = auth.getName(session['username'])
        if auth.admin(session['username']):
            if method == 'GET':
                return render_template('adminAcc',name = name)
        elif method == 'GET':
            return render_template('acc',name = name)       
    return redirect(url_for('login'))

@app.route('/post',methods =['GET','POST'])
def post(link):
    if request.method=='GET':
        return render_template('post.html',text=posts.single(link))

@app.route('/write',methods=['GET','POST'])
def write():
    if request.method=='GET':
        return render_template('write.html')
    elif request.method == 'POST':
        t = request.form['Title']
        p = request.form['Post']
        ti = strftime("%X %x")
        if not posts.write(t,ti,p):
            return "another post with the same title exist" + render_template('write.html')

@app.route('/delete')
def delete():
    posts.delete(link)
    return redirect(url_for('myacc'))
